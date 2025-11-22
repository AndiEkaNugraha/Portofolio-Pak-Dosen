# Memulai dari image Odoo 19.0 resmi
FROM odoo:19.0

# Ganti user menjadi root untuk bisa install paket
USER root

# Install library python yang dibutuhkan untuk modul akuntansi
RUN pip install qifparse --break-system-packages

# Kembalikan user ke odoo untuk keamanan
USER odoo