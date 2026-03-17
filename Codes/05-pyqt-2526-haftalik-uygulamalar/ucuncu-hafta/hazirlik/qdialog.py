import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QDialog, QLineEdit, QDialogButtonBox
)
from PyQt5.QtCore import Qt


class GirisDialogu(QDialog):
    """Kullanıcı adı ve şifre alan özel diyalog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Giriş")
        self.setFixedSize(300, 180)
        self._kur()

    def _kur(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 15, 20, 15)

        layout.addWidget(QLabel("Kullanıcı Adı:"))
        self.kullaniciInput = QLineEdit()
        self.kullaniciInput.setPlaceholderText("admin")
        layout.addWidget(self.kullaniciInput)

        layout.addWidget(QLabel("Şifre:"))
        self.sifreInput = QLineEdit()
        self.sifreInput.setPlaceholderText("••••••")
        self.sifreInput.setEchoMode(QLineEdit.Password)   # Şifre modu
        layout.addWidget(self.sifreInput)

        # Standart OK / İptal butonları
        butonlar = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        butonlar.accepted.connect(self.accept)   # OK → kabul sinyali
        butonlar.rejected.connect(self.reject)   # İptal → ret sinyali
        layout.addWidget(butonlar)

    def girisBilgileri(self):
        """Diyalog kapandıktan sonra değerleri döner."""
        return self.kullaniciInput.text(), self.sifreInput.text()

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDialog Örneği")
        self.setGeometry(200, 200, 450, 250)

        merkez = QWidget()
        self.setCentralWidget(merkez)
        layout = QVBoxLayout(merkez)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        self.sonucLabel = QLabel("Henüz giriş yapılmadı.")
        self.sonucLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sonucLabel)

        btn = QPushButton("Giriş Dialogunu Aç")
        btn.clicked.connect(self._dialogAc)
        layout.addWidget(btn)

    def _dialogAc(self):
        dialog = GirisDialogu(self)             # parent=self → modal olur

        # exec_() → diyalogu MODAL gösterir (ana pencere kilitlenir)
        if dialog.exec_() == QDialog.Accepted:
            kullanici, sifre = dialog.girisBilgileri()
            if kullanici == "admin" and sifre == "1234":
                self.sonucLabel.setText(f"Hoş geldin, {kullanici}!")
            else:
                self.sonucLabel.setText("Hatalı kullanıcı adı veya şifre!")
        else:
            self.sonucLabel.setText("Giriş iptal edildi.")


app = QApplication(sys.argv)
pencere = AnaPencere()
pencere.show()
sys.exit(app.exec_())
