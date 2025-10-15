# apps/users/models.py
from django.db import models, connection

class MTransaksi(models.Model):
    class Meta:
        managed = False  # Django tidak membuat/migrasi tabel ini

    @staticmethod
    def cek_kelolaan(id_user):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) AS data_kelolaan
                FROM tbl_user_marketing a
                LEFT JOIN tbl_mapping_ots b ON a.id_user = b.id_user
                WHERE a.id_user = %s AND b.is_closing = 'C'
            """, [id_user])
            row = cursor.fetchone()
            return row[0] if row else 0

    @staticmethod
    def get_total_ots(data):
        id_user_global = ["63"]
        if str(data.get("id_user")) in id_user_global:
            where_clause = ""
            params = []
        else:
            where_clause = "AND b.id_user = %s"
            params = [data.get("id_user")]

        query = f"""
            SELECT COUNT(*) AS total
            FROM tbl_nominatif a
            JOIN tbl_mapping_ots b ON a.id_pinjaman = b.id_pinjaman
            JOIN tbl_user_marketing c ON c.id_user = b.id_user
            WHERE a.status_pinjaman = 'Aktif'
              AND b.is_closing = 'C'
              AND c.is_aktif = 'Y'
              {where_clause}
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def kategori_ots():
        query = "SELECT * FROM tbl_ots_kategori"
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_reject_cdm(data):
        id_user_global = ["63"]
        if str(data.get("id_user")) in id_user_global:
            where_clause = ""
            params = []
        else:
            where_clause = "AND b.id_user = %s"
            params = [data.get("id_user")]

        query = f"""
            SELECT COUNT(*) AS total
            FROM tbl_nominatif a
            INNER JOIN tbl_mapping_ots b ON a.id_pinjaman = b.id_pinjaman
            INNER JOIN tbl_user_marketing c ON c.id_user = b.id_user
            INNER JOIN tbl_angsuran_approved_wilayah d ON d.id_pinjaman = b.id_pinjaman
            WHERE a.status_pinjaman = 'Aktif'
              AND b.is_closing = 'C'
              AND c.is_aktif = 'Y'
              AND d.is_approved = 'N'
              {where_clause}
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_instansi():
        query = "SELECT COUNT(*) AS total FROM tbl_instansi_pks WHERE is_verifie = 'Y'"
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_validasi():
        query = """
            SELECT COUNT(*) AS total
            FROM tbl_nasabah
            WHERE is_validate = '1' AND is_pks = '1' AND deleted_at IS NULL
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_data_verifikasi(id_user):
        id_user_special = ["47", "2", "63"]
        if str(id_user) in id_user_special:
            where_clause = "AND c.id_product != 5"
            params = []
        else:
            where_clause = "AND c.created_by = %s"
            params = [id_user]

        query = f"""
            SELECT COUNT(*) AS total
            FROM tbl_pinjaman a
            LEFT JOIN tbl_pinjaman_approved b ON a.id = b.id_pinjaman
            JOIN tbl_validasi_borrower c ON c.id_borrower = a.id_nasabah
            WHERE a.status = 0
              AND b.deleted_at IS NULL
              AND a.deleted_at IS NULL
              AND c.deleted_at IS NULL
              {where_clause}
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_data_nonval(id_user):
        id_user_special = ["47", "2", "63"]
        if str(id_user) in id_user_special:
            where_clause = ""
            params = []
        else:
            where_clause = "AND c.created_by = %s"
            params = [id_user]

        query = f"""
            SELECT COUNT(*) AS total
            FROM tbl_pinjaman_approved a
            JOIN tbl_pinjaman b ON a.id_pinjaman = b.id
            LEFT JOIN tbl_validasi_borrower c ON c.id_borrower = b.id_nasabah
            LEFT JOIN tbl_instansi_pks d ON d.id_instansi = c.id_instansi
            LEFT JOIN tbl_nasabah e ON e.id = c.id_borrower
            LEFT JOIN tbl_pinjaman_approved_caad f ON f.id_pinjaman = a.id_pinjaman
            WHERE (a.is_valid = 'N' 
                   AND b.status = 0 
                   AND b.id = (
                       SELECT MAX(tp.id) 
                       FROM tbl_pinjaman tp 
                       WHERE tp.id_nasabah = e.id
                   ))
              AND a.deleted_at IS NULL 
              AND c.deleted_at IS NULL
              {where_clause}
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_data_pinjaman(id_user, status):
        id_user_special = ["47", "2", "63"]
        if str(id_user) in id_user_special:
            where_clause = ""
            params = []
        else:
            where_clause = "AND c.created_by = %s"
            params = [id_user]

        if isinstance(status, list):
            placeholders = ", ".join(["%s"] * len(status))
            status_params = status
        else:
            placeholders = "%s"
            status_params = [status]

        params = status_params + params

        query = f"""
            SELECT COUNT(*) AS total
            FROM tbl_pinjaman a
            JOIN tbl_nasabah b ON a.id_nasabah = b.id
            LEFT JOIN tbl_validasi_borrower c ON c.id_borrower = a.id_nasabah
            WHERE a.status IN ({placeholders})
              AND c.deleted_at IS NULL
              AND a.deleted_at IS NULL
              AND c.is_verifie = 'Y'
              {where_clause}
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        
    def get_data_pinjaman_kredit_berjalan(id_user):
        """
        Menghitung total pinjaman kredit berjalan berdasarkan id_user
        dengan query raw SQL yang aman dan list of dict sebagai output.
        """
        id_user_special = ["47", "2", "63"]

        if str(id_user) in id_user_special:
            # Query untuk user special
            query = """
                SELECT COUNT(*) AS total,
                    IF(b.status = 6, 'L',
                        IF(
                            (SELECT ROUND(oj.outstanding)
                            FROM tbl_angsuran_ojk oj
                            WHERE oj.noPinjaman = b.id
                            AND oj.tgl_bayar IS NOT NULL
                            ORDER BY oj.tgl DESC
                            LIMIT 1
                            ) = 0, 'L', 'O'
                        )
                    ) AS status_pinjaman
                FROM tbl_nasabah a
                JOIN tbl_pinjaman b ON a.id = b.id_nasabah
                JOIN tbl_angsuran_ojk c ON c.noPinjaman = b.id
                LEFT JOIN tbl_log_fdc d ON d.id_pinjaman = b.id
                LEFT JOIN tbl_nominatif e ON e.id_pinjaman = b.id
                LEFT JOIN tbl_agregator f ON f.id_agregator = e.id_agregator
                LEFT JOIN tbl_pendanaan_loan g ON g.id_pinjaman = b.id
                WHERE a.nipBaru NOT IN (%s, %s, %s, %s)
                AND a.deleted_at IS NULL
                AND b.deleted_at IS NULL
                AND b.status IN (5,6)
                AND f.id_agregator != 4
                GROUP BY b.id
            """
            params = [
                '123456789123456789',
                '123456789987654321',
                '123456789987654322',
                '12345678910123456'
            ]
        else:
            # Query untuk user biasa
            query = """
                SELECT COUNT(*) AS total
                FROM tbl_nominatif a
                JOIN tbl_pinjaman b ON a.id_pinjaman = b.id
                LEFT JOIN tbl_validasi_borrower c ON c.id_borrower = b.id_nasabah
                WHERE b.status = %s
                AND c.deleted_at IS NULL
                AND b.deleted_at IS NULL
                AND a.deleted_at IS NULL
                AND b.status_debitur = 0
                AND c.created_by = %s
                GROUP BY a.id_pinjaman
            """
            params = [5, id_user]

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in result]
        
    def get_ttd(id_user):
        """
        Menghitung total pinjaman yang belum ditandatangani (TTD)
        berdasarkan id_user, menggunakan raw SQL aman.
        """
        id_user_special = ["47", "2", "63"]

        if str(id_user) in id_user_special:
            where_clause = ""
            params = []
        else:
            where_clause = "AND c.created_by = %s"
            params = [id_user]

        query = f"""
            SELECT COUNT(*) AS total
            FROM tbl_pinjaman a
            LEFT JOIN tbl_privy_dokumen b ON a.id = b.id_pinjaman
            LEFT JOIN tbl_validasi_borrower c ON c.id_borrower = a.id_nasabah
            LEFT JOIN tbl_teken_aja d ON d.id_pinjaman = a.id
            WHERE a.deleted_at IS NULL
            AND a.status = 2
            AND c.deleted_at IS NULL
            AND IF(a.is_ttd = 'teken', d.sign_pk, b.sign_pk) = 'N'
            {where_clause}
        """

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in result]
        
    def get_pencairan(id_user):
        """
        Menghitung total pencairan pinjaman berdasarkan id_user
        menggunakan raw SQL yang aman dan list of dict sebagai output.
        """
        id_user_special = ["47", "2", "63"]

        if str(id_user) in id_user_special:
            where_clause = ""
            params = []
        else:
            where_clause = "AND c.created_by = %s"
            params = [id_user]

        query = f"""
            SELECT COUNT(*) AS total
            FROM tbl_pinjaman a
            LEFT JOIN tbl_pinjaman_approved b ON a.id = b.id_pinjaman
            JOIN tbl_validasi_borrower c ON c.id_borrower = a.id_nasabah
            LEFT JOIN tbl_instansi_pks d ON d.id_instansi = c.id_instansi
            LEFT JOIN tbl_nasabah e ON e.id = c.id_borrower
            LEFT JOIN tbl_instansi_pks f ON f.id_instansi = c.id_instansi
            LEFT JOIN tbl_user_marketing g ON g.id_user = c.created_by
            LEFT JOIN tbl_product h ON h.id_product = c.id_product
            LEFT JOIN tbl_pendanaan_loan i ON i.id_pinjaman = a.id
            LEFT JOIN tbl_approved_detail j ON j.id_pinjaman = a.id
            WHERE a.status = 2
            AND c.deleted_at IS NULL
            AND b.deleted_at IS NULL
            AND i.id_pinjaman IS NULL
            AND a.deleted_at IS NULL
            AND j.ket LIKE '%%Direct Pencairan%%'
            {where_clause}
        """

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in result]
    
    def total_dpk(id_user):
        """
        Menghitung total debitur (DPK) berdasarkan id_user
        menggunakan raw SQL aman dan list of dict sebagai output.
        """
        query = """
            SELECT COUNT(*) AS total_debitur
            FROM tbl_nominatif a
            LEFT JOIN tbl_pinjaman b ON a.id_pinjaman = b.id
            LEFT JOIN tbl_validasi_borrower c ON b.nipBaru = c.nip
            WHERE c.created_by = %s
            AND c.deleted_at IS NULL
            AND a.status_pinjaman = 'Aktif'
            AND b.status_debitur = 0
            AND b.deleted_at IS NULL
        """

        params = [id_user]

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in result]

    def cek_login(id_user, app_name, versi):
        """
        Mengecek login user marketing dan konfigurasi aplikasi.
        Menggunakan raw SQL aman dari SQL Injection.
        """
        result = {}

        # Cek user
        query_user = "SELECT * FROM tbl_user_marketing WHERE id_user = %s"
        with connection.cursor() as cursor:
            cursor.execute(query_user, [id_user])
            user_rows = cursor.fetchall()
            user_columns = [col[0] for col in cursor.description]

        if not user_rows:
            raise ValueError("User tidak ditemukan")

        data_user = dict(zip(user_columns, user_rows[0]))

        # Cek konfigurasi
        query_config = "SELECT * FROM tbl_config WHERE app_name = %s AND versionName = %s"
        with connection.cursor() as cursor:
            cursor.execute(query_config, [app_name, versi])
            config_rows = cursor.fetchall()
            config_columns = [col[0] for col in cursor.description]

        if not config_rows:
            raise ValueError("Konfigurasi aplikasi atau versi tidak ditemukan")

        config_data = dict(zip(config_columns, config_rows[0]))

        # Kembalikan hasil
        result = {
            "status": True,
            "message": "Login dan versi berhasil",
            "data_user": data_user,
            "config_data": config_data
        }

        return result
        
    
