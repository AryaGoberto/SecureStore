document.addEventListener('DOMContentLoaded', () => {
    const loginContent = document.querySelector('.login-content');
    const registerContent = document.querySelector('.register-content');
    const signupLink = document.getElementById('signup-link');
    const signinLink = document.getElementById('signin-link');

    if (loginContent && registerContent) {
        // Pastikan konten login aktif saat halaman dimuat
        loginContent.classList.add('active');
        registerContent.classList.remove('active'); // Pastikan register tidak aktif

        // HAS-CONTENT
        const inputFields = document.querySelectorAll('.input-field');

        inputFields.forEach(input => {
            // Cek saat halaman pertama kali dimuat
            if (input.value.length > 0) {
                input.classList.add('has-content');
            }

            // Tambah event listener untuk setiap input
            input.addEventListener('input', function() {
                if (this.value.length > 0) {
                    this.classList.add('has-content');
                } else {
                    this.classList.remove('has-content');
                }
            });
        });
        // BATAS HAS-CONTENT

        signupLink.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Animasi login content keluar ke kiri
            loginContent.classList.add('inactive-left');
            loginContent.classList.remove('active'); // Hapus aktif setelah memulai transisi keluar
            
            // Setelah transisi keluar selesai, reset posisi login content dan tampilkan register content
            setTimeout(() => {
                loginContent.classList.remove('inactive-left'); // Reset posisi untuk transisi berikutnya
                // Animasi register content masuk dari kanan
                registerContent.classList.add('active');
                // Pastikan registerContent tidak memiliki kelas inactive-right jika ada
                registerContent.classList.remove('inactive-right');
            }, 600); // Sesuaikan dengan durasi transisi CSS (0.6s = 600ms)
        });

        signinLink.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Animasi register content keluar ke kanan
            registerContent.classList.add('inactive-right');
            registerContent.classList.remove('active'); // Hapus aktif setelah memulai transisi keluar

            // Setelah transisi keluar selesai, reset posisi register content dan tampilkan login content
            setTimeout(() => {
                registerContent.classList.remove('inactive-right'); // Reset posisi untuk transisi berikutnya
                // Animasi login content masuk dari kiri (sudah default posisinya)
                loginContent.classList.add('active');
                // Pastikan loginContent tidak memiliki kelas inactive-left jika ada
                loginContent.classList.remove('inactive-left');
            }, 600); // Sesuaikan dengan durasi transisi CSS (0.6s = 600ms)
        });
    }
    
    // --- KODE UNTUK DROPDOWN SETTINGS DARI SEBELUMNYA ---
    // (biarkan kode yang sudah ada)


    // --- KODE BARU UNTUK UPLOAD FOTO PROFIL ---
    const profilePicInput = document.getElementById('foto-profil');
    const picDisplay = document.getElementById('profile-pic-display');
    const fileNameDisplay = document.getElementById('file-name-display');

    // Cek apakah elemen-elemen ini ada di halaman saat ini
    if (profilePicInput && picDisplay && fileNameDisplay) {
        
        // Tambahkan event listener: jika ada file yang dipilih...
        profilePicInput.addEventListener('change', function(event) {
            const file = event.target.files[0];

            if (file) {
                // Tampilkan nama file
                fileNameDisplay.textContent = file.name;

                // Tampilkan preview gambar
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Set background dari div preview dengan gambar yang dipilih
                    picDisplay.style.backgroundImage = `url('${e.target.result}')`;
                    // Hilangkan ikon '+'
                    picDisplay.innerHTML = ''; 
                }
                reader.readAsDataURL(file);

            } else {
                // Jika tidak ada file dipilih, kembalikan ke semula
                fileNameDisplay.textContent = 'Tidak ada file dipilih';
                picDisplay.style.backgroundImage = 'none';
                picDisplay.innerHTML = '<i class="fas fa-user-plus"></i>';
            }
        });

        // Membuat label tombol juga bisa diakses dengan keyboard
        const uploadLabel = document.querySelector('label[for="foto-profil"]');
        if (uploadLabel) {
            uploadLabel.addEventListener('keydown', function(event) {
                if (event.key === 'Enter' || event.key === ' ') {
                    profilePicInput.click();
                }
            });
        }
    }

    // --- KODE BARU UNTUK VALIDASI KONFIRMASI PASSWORD ---
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('konfirmasi-password');
    const passwordError = document.getElementById('password-error');
    const userForm = document.querySelector('.main-form'); // Menargetkan form

    // Fungsi untuk mengecek apakah password cocok
    function validatePassword() {
        if (passwordInput.value !== confirmPasswordInput.value) {
            // Jika tidak cocok
            passwordError.textContent = 'Konfirmasi password tidak cocok!';
            passwordError.style.display = 'block'; // Tampilkan pesan error
            confirmPasswordInput.classList.add('input-error'); // Tambahkan border merah
            return false; // Kembalikan nilai false
        } else {
            // Jika cocok
            passwordError.textContent = '';
            passwordError.style.display = 'none'; // Sembunyikan pesan error
            confirmPasswordInput.classList.remove('input-error'); // Hapus border merah
            return true; // Kembalikan nilai true
        }
    }

    // Cek apakah elemen-elemen ini ada di halaman
    if (passwordInput && confirmPasswordInput && passwordError && userForm) {
        
        // Jalankan validasi setiap kali user mengetik di salah satu kolom
        passwordInput.addEventListener('keyup', validatePassword);
        confirmPasswordInput.addEventListener('keyup', validatePassword);

        // Tambahkan pengecekan terakhir saat form akan disubmit
        userForm.addEventListener('submit', function(event) {
            // Jika validasi password gagal...
            if (!validatePassword()) {
                // ...maka batalkan pengiriman form
                event.preventDefault();
                alert('Gagal menyimpan! Pastikan konfirmasi password sudah benar.');
            }
        });
    }
});