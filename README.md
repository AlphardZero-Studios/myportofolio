Nama : Alphard Qodaruddin
NPM : 2506632910
Kelas : PBP F

### Tugas 1

1. Ya saya menggunakan elemen semantik HTML5 tersebut.  Elemen-elemen ini membantu saya agar struktur kode bisa lebih terorganisir dengan memisahkan bagian seperti Hero, Projects, Skills, dan Experience ke dalam tag <section> dengan id masing-masing.
2. Tantangan terbesar ada pada pengaturan layout yang memiliki multiple kolom seperti grid pada bagian Hero dan bagian Experience. Di tampilan desktop, foto dan teks berdampingan secara horizontal, namun di layar HP tata letak tersebut menjadi terlalu sempit dan memakan ruang horizontal, sehingga saya melakukan pengurutan prioritas posisi dan ukuran sesuai denagn urutan keterbacaan utama, orientasi elemennya, dan fleksibilitas grid tersebut.
3. Batasan yang saya sangat rasakan adalah pada saat setiap kali ada perubahan data, saya harus merubah dan hardcode file HTML secara langsung, belum memakai sistem seperti "variable" di programming yang mana tidak perlu saya hardcode file aslinya untuk mengubah data. Sehingga iterasi selanjutnya saya mau masukkan Django Admin Panel agar proyek bisa ditambah, diedit, atau dihapus langsung melalui Django Admin tanpa menyentuh file HTML.

## AI Disclosure Tugas 1:
Saya menggunakan bantuan AI  (ChatGPT & Gemini) dalam mengerjakan tugas ini HANYA untuk membantu saya memahami struktur project untuk mendesain dan menambahkan fitur, mencari tahu apa saja teknik yang bisa saya lakukan, memahami bagaimana syntax yang bisa saya gunakan, dan strategi workflow step by step seperti apa yang harus saya lakukan agar pengerjaannya bisa efektif. Prompt yang saya gunakan adalah:
	- ChatGPT: "i am currently building a website in django, i have no prior knowledge in making a website except just simpe html and css. currently the website is already running but idk how to design it, like where can i design it visually? im a graphic designer preferable using figma btw"
	- Gemini: "im currently making a portfolio website with django, still beginner, give me some options to add new features and section into the website, and i will pick, then you will tell me how to make it. keep everything still simple and very beginner, dont add some itermediate or advanced things"

### Tugas 2

1. Ketika pengguna membuka halaman portofolio saya, alurnya seperti ini:
	1. Browser membuka link dan mengirim HTTP request GET ke link tersebut (get ini bisa terlihat di console terminal)
	2. Django akan membuka urls.py yang ada di subfolder "portofolio", lalu mengarahkan ke file url yaitu urls.py yang ada di subfolder aplikasi "main"
	3. views.py yang ada di subfolder "main" langsung memproses halaman utama untuk mulai render
	4. Model mengambil data yang diperlukan dari database
	5. Template menampilkan hasil render dan memasukkan data yang didapat dari model, lalu mengaplikasikan css stylingnya
2. Data portofolio disimpan di model karena model bertugas untuk mengelola semua data yang ada, dan template hanya bertugas untuk menampilkan data. Ini memudahkan maintenance websitenya karena tidak ada data yang di hardcode langsung pada tampilan, membuatnya menjadi mudah untuk melakukan perubahan pada data maupun penambahan data pada skala long-term. Lalu template juga cukup menggunakan for loops untuk menampilkan data yang banyak secara otomatis, membuat html file lebih ringkas. Semua ini dilakukan agar aplikasi memiliki struktur yang mudah dipahami dalam jangka panjang.
3. makemigrations adalah command untuk mempersiapkan perubahan untuk direview kembali sebelum benar benar diapply, sehingga database sama sekali belum disentuh. Sedangkan migrate adalah command untuk menerapkan perubahan tersebut ke database yang sebenarnya. Analogi yang saya suka gunakan adalah makemigration seperti git add atau git commit, dan migrate seperti git push.
	Contoh perubahan:
	Misal di awal, models.py isinya seperti ini:
			class Experience(models.Model):
			EXPERIENCE_CHOICES = [
				('internship', 'Internship'),
				('full-time', 'Full-Time'),
				('freelance', 'Freelance'),
			]
			id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
			title = models.CharField(max_length=255)
	Kemudian saya ubah dengan menambahkan baris baru:
			description = models.TextField()
	Perubahan ini harus saya lakukan makemigration dulu sebelum bisa benar benar diterapkan menggunakan migrate.

## AI Disclosure Tugas 2:
Saya sama sekali TIDAK MENGGUNAKAN AI dalam mengerjakan tugas 2 ini, seluruh hasil kerja yang saya lakukan pada tugas kali ini murni hasil buatan saya sendiri, hanya berbekalkan Tutorial 2. Beberapa hal seperti styling css dan format model saya mengcopy apa yang pernah saya lakukan dari tugas-tugas dan tutorial sebelumnya, yang kemudian saya modifikasi sendiri melalui trial dan error.

### Tugas 3
1. Menggunakan ModelForm akan jauh lebih efisien karena saya tidak perlu lagi menulis kode HTML berulangkali dan panjang untuk setiap form. ModelForm akan membuatkan kolom input secara otomatis tergantung dengan tipe data yang dipilih, bisa memvalidasi juga apakh inputnya benar atau tidak, dan juga lebih aman dari error pada menyimpan data. Lalu saya harus menggunakan tag {% csrf_token %} untuk setiap form POST demi keamanan website saya, karena tanpa token tersebut, hacker bisa saja mengirimkan data palsu dan mengotak-atik isi database saya.
2. JSON lebih disukai oleh banyak orang (termasuk saya hehe) karena strukturnya sederhana, mudah dimengerti, berbentuk seperti dictionary dimana ada pasangan key-value, ukurannya lebih kecil, dan lebih cepat diproses juga.
3. Alurnya seperti ini:
	1. HTTP Request menggunakan GET ke server
	2. Mengecek URL mana yang cocok dengan GET tersebut lalu lanjut ke file view yang sesuai
	3. Fungsi pada view mengambil data dari database yang berupa object QuerySet
	4. object QuerySet tersebut dikonversi menjadi tipe data yang biasa digunakan python, proses ini disebut serialization
	5. Data python yang didapatkan kemudian diubah menjadi JSON, kemudian dikirim kembali ke pengguna.
Mengapa harus serialization: karena format database dan django hasilnya tipe data "spesial" yang kompleks dan butuh di"translate" terlebih dulu menjadi bentuk tipe data yang bisa dibaca python, baru setelah itu python bisa mengubahnya menjadi json.

## AI Disclosure Tugas 3:
Sama seperti tugas 2, saya sama sekali TIDAK MENGGUNAKAN AI dalam mengerjakan tugas 3 ini, seluruh hasil kerja yang saya lakukan pada tugas kali ini murni hasil buatan saya sendiri, hanya berbekalkan Tutorial 3 dan beberapa website sumber belajar dasar django dari internet. Beberapa hal seperti styling css dan format model saya mengcopy apa yang pernah saya lakukan dari tugas-tugas dan tutorial sebelumnya, yang kemudian saya modifikasi sendiri melalui trial dan error.