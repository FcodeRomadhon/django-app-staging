# apps/api/v1/users/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import MTransaksi
import logging

logger = logging.getLogger('users')

@api_view(['POST'])
def dashboard_api_view(request):
    try:
        data = request.data
        user_id = data.get('id_user')
        app_versi = data.get('app_versi', "VERVAL,2.1.0")
        if not user_id:
            logger.warning("❌ id_user missing in request")
            return Response({
                "status": False,
                "message": "id_user wajib dikirim",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

        # Parse versi app
        parts = app_versi.split(',')
        req_data = {
            'id_user': user_id,
            'app': parts[0],
            'versi': parts[1]
        }

        hasil = {}
        kategori_ots = []

        # ===== Data Kelolaan OTS =====
        kelolaan_count = MTransaksi.cek_kelolaan(user_id)
        data_kelolaan = {}
        if kelolaan_count > 0:
            total_ots_list = MTransaksi.get_total_ots(req_data)
            total_ots = total_ots_list[0]['total'] if total_ots_list else 0
            kategori_ots = MTransaksi.kategori_ots()
            data_kelolaan.update({
                'total': total_ots,
                'title': "Data Kelolaan",
                'visible': True
            })
        else:
            data_kelolaan.update({
                'total': 0,
                'title': "Data Kelolaan",
                'visible': False
            })

        # ===== Data Reject CDM =====
        data_reject_list = MTransaksi.get_reject_cdm(req_data)
        data_reject = {
            'total': data_reject_list[0]['total'] if data_reject_list else 0,
            'title': "Data Reject CDM",
            'visible': bool(data_reject_list)
        }

        # ===== Total instansi =====
        instansi_list = MTransaksi.get_instansi()
        instansi = {
            'total': instansi_list[0]['total'] if instansi_list else 0,
            'title': "Instansi Terdaftar",
            'visible': bool(instansi_list)
        }

        # ===== Total Validasi borrower =====
        validasi_list = MTransaksi.get_validasi()
        validasi = {
            'total': validasi_list[0]['total'] if validasi_list else 0,
            'title': "Validasi Borrower",
            'visible': bool(validasi_list)
        }

        # ===== Total Data Verifikasi =====
        verifikasi_list = MTransaksi.get_data_verifikasi(user_id)
        verifikasi = {
            'total': verifikasi_list[0]['total'] if verifikasi_list else 0,
            'title': "Data Verifikasi",
            'visible': bool(verifikasi_list)
        }

        # ===== Total Data Non Valid =====
        nonval_list = MTransaksi.get_data_nonval(user_id)
        nonval = {
            'total': nonval_list[0]['total'] if nonval_list else 0,
            'title': "Data Non Valid",
            'visible': bool(nonval_list)
        }

        # ===== Data Pengajuan Peminjam =====
        pengajuan_list = MTransaksi.get_data_pinjaman(user_id, status=1)
        pengajuan = {
            'total': pengajuan_list[0]['total'] if pengajuan_list else 0,
            'title': "Pengajuan Peminjam",
            'visible': bool(pengajuan_list)
        }

        # ===== Data Proses =====
        proses_list = MTransaksi.get_data_pinjaman(user_id, status=7)
        proses = {
            'total': proses_list[0]['total'] if proses_list else 0,
            'title': "Proses",
            'visible': bool(proses_list)
        }

        # ===== Kredit Berjalan =====
        kredit_list = MTransaksi.get_data_pinjaman_kredit_berjalan(user_id)
        kredit_berjalan = {
            'total': len(kredit_list) if kredit_list else 0,
            'title': "Data Kredit Berjalan",
            'visible': bool(kredit_list)
        }

        # ===== TTD Digital =====
        ttd_list = MTransaksi.get_ttd(user_id)
        ttd_digital = {
            'total': ttd_list[0]['total'] if ttd_list else 0,
            'title': "Menunggu TTD Digital",
            'visible': bool(ttd_list)
        }

        # ===== Pencairan =====
        pencairan_list = MTransaksi.get_pencairan(user_id)
        pencairan = {
            'total': pencairan_list[0]['total'] if pencairan_list else 0,
            'title': "Proses Pencairan",
            'visible': bool(pencairan_list)
        }

        # ===== Kualitas Kredit =====
        kualitas_list = MTransaksi.total_dpk(user_id)
        kualitas_kredit = {
            'total': kualitas_list[0]['total_debitur'] if kualitas_list else 0,
            'title': "Kualitas Kredit",
            'visible': bool(kualitas_list)
        }

        # ===== Cek Login =====
        result_cek = MTransaksi.cek_login(user_id, req_data['app'], req_data['versi'])
        user_data = result_cek['data_user']
        config_data = result_cek['config_data']

        if config_data['is_active'] == "N":
            logger.info(f"✅ Returning config-only for user_id={user_id}")
            return Response({
                "status": True,
                "message": "Data Versi Active",
                "data": config_data
            })

        # ===== Gabungkan hasil sesuai akses_level =====
        if user_data['is_aktif'] == "Y" and user_data['akses_level'] in ["RO", "FC"]:
            hasil['data_kelolaan'] = data_kelolaan
            hasil['data_reject'] = data_reject
            hasil['kategori'] = kategori_ots
        else:
            data_ots = {'total': 0, 'title': "OTS Prospek", 'visible': True}
            hasil.update({
                "instansi_terdaftar": instansi,
                "validasi_peminjam": validasi,
                "verifikasi": verifikasi,
                "nonval": nonval,
                "pengajuan": pengajuan,
                "proses": proses,
                "ttd_digisign": ttd_digital,
                "pencairan": pencairan,
                "kredit_berjalan": kredit_berjalan,
                "kualitas_kredit": kualitas_kredit,
                "data_kelolaan": data_kelolaan,
                "data_reject": data_reject,
                "data_ots": data_ots,
                "kategori": kategori_ots
            })

        logger.info(f"✅ Dashboard response sent for user_id={user_id}")
        return Response({
            "status": True,
            "message": "Data dashboard berhasil.",
            "data": hasil
        })

    except Exception as e:
        logger.error(f"❌ dashboard_api_view error: {e}", exc_info=True)
        return Response({
            "status": False,
            "message": "Terjadi kesalahan internal.",
            "data": {}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)