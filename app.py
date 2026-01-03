import random
import sys
import time

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                              QPushButton, QVBoxLayout, QGridLayout, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, QRect, QPointF
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QFont, QPainterPath, QRegion


class HeartButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(200, 180)
        self.is_hovered = False
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Create heart shape mask
        path = QPainterPath()
        width = self.width()
        height = self.height()
        
        # Heart shape using Bezier curves
        # Start at bottom point
        path.moveTo(width / 2, height * 0.9)
        
        # Left side of heart
        path.cubicTo(
            width * 0.1, height * 0.6,  # control point 1
            width * 0.1, height * 0.2,  # control point 2
            width * 0.3, height * 0.15  # end point (top of left bump)
        )
        path.cubicTo(
            width * 0.4, height * 0.1,  # control point 1
            width * 0.5, height * 0.15, # control point 2
            width * 0.5, height * 0.3   # end point (center dip)
        )
        
        # Right side of heart
        path.cubicTo(
            width * 0.5, height * 0.15, # control point 1
            width * 0.6, height * 0.1,  # control point 2
            width * 0.7, height * 0.15  # end point (top of right bump)
        )
        path.cubicTo(
            width * 0.9, height * 0.2,  # control point 1
            width * 0.9, height * 0.6,  # control point 2
            width / 2, height * 0.9     # end point (bottom point)
        )
        
        path.closeSubpath()
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))
    
    def enterEvent(self, event):
        self.is_hovered = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.is_hovered = False
        self.update()
        super().leaveEvent(event)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw heart shape
        path = QPainterPath()
        width = self.width()
        height = self.height()
        
        # Heart shape
        path.moveTo(width / 2, height * 0.9)
        path.cubicTo(
            width * 0.1, height * 0.6,
            width * 0.1, height * 0.2,
            width * 0.3, height * 0.15
        )
        path.cubicTo(
            width * 0.4, height * 0.1,
            width * 0.5, height * 0.15,
            width * 0.5, height * 0.3
        )
        path.cubicTo(
            width * 0.5, height * 0.15,
            width * 0.6, height * 0.1,
            width * 0.7, height * 0.15
        )
        path.cubicTo(
            width * 0.9, height * 0.2,
            width * 0.9, height * 0.6,
            width / 2, height * 0.9
        )
        path.closeSubpath()
        
        # Fill color based on hover state
        if self.is_hovered:
            painter.setBrush(QColor("#FFC1CC"))
        else:
            painter.setBrush(QColor("#ED1F64"))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
        # Draw text
        if self.is_hovered:
            painter.setPen(QColor("#000000"))
        else:
            painter.setPen(QColor("#FFFFFF"))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())


class StartMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test: Tabla Inmultirii")
        self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(500, 400)
        
        # Central widget with gradient background
        self.central_widget = GradientWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Test de Tabla Inmultirii")
        title.setFont(QFont("Helvetica", 42, QFont.Weight.Bold))
        title.setStyleSheet("color: #5A375A; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(20)
        
        # Subtitle
        subtitle = QLabel("Alege numarul de intrebari:")
        subtitle.setFont(QFont("Helvetica", 24))
        subtitle.setStyleSheet("color: #5A375A; background: transparent;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        
        # Buttons for different question counts
        question_options = [10, 25, 50, 100]
        for num in question_options:
            btn = QPushButton(f"{num} intrebari")
            btn.setFont(QFont("Helvetica", 20))
            btn.setMinimumSize(250, 60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ED1F64;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #FFC1CC;
                    color: #000000;
                }
            """)
            btn.clicked.connect(lambda checked, n=num: self.start_quiz(n))
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addSpacing(10)
        
        self.central_widget.setLayout(layout)
    
    def start_quiz(self, num_questions):
        self.quiz_window = MultiplicationQuiz(num_questions)
        self.quiz_window.show()
        self.close()


class MultiplicationQuiz(QMainWindow):
    def __init__(self, total_questions):
        super().__init__()
        self.total_questions = total_questions
        super().__init__()
        self.setWindowTitle("Test de Tabla Inmultirii")
        self.setGeometry(100, 100, 900, 650)
        self.setMinimumSize(1200, 950)

        self.score = 0
        self.current_question = 0
        self.wrong_answers = []  # Track wrong answers
        
        # Timer variables
        self.start_time = None
        self.elapsed_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        # Central widget with gradient background
        self.central_widget = GradientWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Main frame for question widgets
        self.main_frame = QWidget()
        self.main_frame.setStyleSheet("background: transparent;")
        main_layout.addWidget(self.main_frame, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        # Timer label at top
        self.timer_label = QLabel("Timp: 00:00")
        self.timer_label.setStyleSheet("color: #5A375A; background: transparent;")
        self.timer_label.setFont(QFont("Helvetica", 24, QFont.Weight.Bold))
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.timer_label)
        
        # Score label at bottom
        self.score_label = QLabel(f"Scor: {self.score}")
        self.score_label.setStyleSheet("color: #FFC1CC; background: transparent;")
        self.score_label.setFont(QFont("Helvetica", 46))
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
        main_layout.addWidget(self.score_label)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.central_widget.setLayout(main_layout)

        # Build question widgets
        self.build_question_widgets()

        # Start first question
        self.new_question()

    # ---------------- Build Question Widgets ----------------
    def build_question_widgets(self):
        # Clear existing layout
        if self.main_frame.layout():
            QWidget().setLayout(self.main_frame.layout())
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Question label
        self.question_label = QLabel()
        self.question_label.setFont(QFont("Helvetica", 46, QFont.Weight.Bold))
        self.question_label.setStyleSheet("color: #FFC1CC; background: transparent;")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.question_label)
        layout.addSpacing(20)
        
        # Buttons grid
        buttons_widget = QWidget()
        buttons_widget.setStyleSheet("background: transparent;")
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(10)
        
        self.buttons = []
        for i in range(4):
            btn = HeartButton()
            btn.setFont(QFont("Helvetica", 28, QFont.Weight.Bold))
            btn.setMinimumSize(220, 200)
            btn.clicked.connect(lambda checked, x=i: self.check_answer(x))
            buttons_layout.addWidget(btn, i // 2, i % 2)
            self.buttons.append(btn)
        
        buttons_widget.setLayout(buttons_layout)
        layout.addWidget(buttons_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(15)
        
        # Feedback label
        self.feedback_label = QLabel()
        self.feedback_label.setFont(QFont("Helvetica", 46, QFont.Weight.Bold))
        self.feedback_label.setStyleSheet("background: transparent;")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback_label)
        
        self.main_frame.setLayout(layout)
        
        # Update score
        self.score_label.setText(f"Scor: {self.score}")

    # ---------------- Game Logic ----------------
    def new_question(self):
        if self.current_question >= self.total_questions:
            self.timer.stop()  # Stop timer when quiz ends
            self.show_end_screen()
            return

        # Start timer on first question
        if self.current_question == 0:
            self.start_time = time.time()
            self.timer.start(100)  # Update timer every 100ms
        
        self.current_question += 1
        self.feedback_label.setText("")

        self.a = random.randint(1, 10)
        self.b = random.randint(1, 10)
        self.correct_answer = self.a * self.b

        self.question_label.setText(
            f"Intrebarea {self.current_question}/{self.total_questions}\n\n{self.a} × {self.b} = ?"
        )

        answers = [self.correct_answer]
        while len(answers) < 4:
            wrong = random.randint(1, 100)
            if wrong not in answers:
                answers.append(wrong)
        random.shuffle(answers)

        for i, btn in enumerate(self.buttons):
            btn.setText(str(answers[i]))
            btn.answer = answers[i]

    def check_answer(self, index):
        correct_messages = ["Excelent 🦄", "Foarte Bine 🎉", "Ai dreptate 😘", "Te descurci excelent 👏", "Avem un mic geniu printre noi 🧠", "Corect 👏", "O sa ajungi departe 🚀"]
        wrong_messages = ["Aproape bine 🙈", "Nu e bai, mai incearca 🤩", "Se poate intampla oricui 🐵", "Hai ca poti 👸", "Nici eu nu o stiam pe asta 🙊", "Repetitia e mama invataturii 🤩", "Haide, nu te lasa 💪"]
        
        if self.buttons[index].answer == self.correct_answer:
            self.score += 1
            self.feedback_label.setText(random.choice(correct_messages))
            self.feedback_label.setStyleSheet("color: #FFC1CC; background: transparent;")
            self.spawn_stars()
        else:
            # Track wrong answer
            self.wrong_answers.append({
                'question': f"{self.a} × {self.b}",
                'correct': self.correct_answer,
                'user_answer': self.buttons[index].answer
            })
            self.feedback_label.setText(random.choice(wrong_messages))
            self.feedback_label.setStyleSheet("color: #C2185B; background: transparent;")

        self.score_label.setText(f"Scor: {self.score}")
        QTimer.singleShot(1000, self.new_question)

    # ---------------- Timer Update ----------------
    def update_timer(self):
        if self.start_time:
            self.elapsed_time = time.time() - self.start_time
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            self.timer_label.setText(f"Timp: {minutes:02d}:{seconds:02d}")
    
    def format_time(self, seconds):
        """Format seconds into MM:SS string"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    # ---------------- End Screen ----------------
    def show_end_screen(self):
        # Clear existing layout
        if self.main_frame.layout():
            QWidget().setLayout(self.main_frame.layout())
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(30, 30, 30, 30)
        
        self.buttons = []

        percentage_score = (self.score / self.total_questions) * 100

        if percentage_score == 100:
            congrats_text = "Esti un geniu! Felicitari! 🌟🌟🌟"
        elif percentage_score >= 75:
            congrats_text = "Excelent! Ai invatat bine! 🎉"
        elif percentage_score >= 50:
            congrats_text = "Bine! Mai exerseaza putin! 👍"
        elif percentage_score >= 25:
            congrats_text = "Nu e rau! Mai incearca! 🤗"
        else:
            congrats_text = "Nu te descuraja! Mai incearca! 💪"

        congrats_label = QLabel(congrats_text)
        congrats_label.setFont(QFont("Helvetica", 42, QFont.Weight.Bold))
        congrats_label.setStyleSheet("color: #5A375A; background: transparent;")
        congrats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(congrats_label)
        layout.addSpacing(20)

        score_text_label = QLabel(f"Scorul tau este: {self.score} puncte din {self.total_questions} ({percentage_score:.2f}%)")
        score_text_label.setFont(QFont("Helvetica", 38))
        score_text_label.setStyleSheet("color: #FFC1CC; background: transparent;")
        score_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(score_text_label)
        layout.addSpacing(10)
        
        # Show time taken
        time_label = QLabel(f"Timp total: {self.format_time(self.elapsed_time)}")
        time_label.setFont(QFont("Helvetica", 32))
        time_label.setStyleSheet("color: #5A375A; background: transparent;")
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(time_label)
        layout.addSpacing(20)
        
        # Show wrong answers if any
        if self.wrong_answers:
            wrong_title = QLabel("Trebuie sa mai repeti:")
            wrong_title.setFont(QFont("Helvetica", 32, QFont.Weight.Bold))
            wrong_title.setStyleSheet("color: #C2185B; background: transparent;")
            wrong_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(wrong_title)
            layout.addSpacing(10)
            
            # Create scrollable area for wrong answers
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setMaximumHeight(200)
            scroll_area.setStyleSheet("""
                QScrollArea {
                    background: transparent;
                    border: 2px solid #C2185B;
                    border-radius: 10px;
                }
                QScrollBar:vertical {
                    background: #FFE6F0;
                    width: 12px;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical {
                    background: #ED1F64;
                    border-radius: 6px;
                }
            """)
            
            # Widget to hold wrong answers
            wrong_widget = QWidget()
            wrong_widget.setStyleSheet("background: transparent;")
            wrong_layout = QVBoxLayout()
            wrong_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            wrong_layout.setContentsMargins(10, 10, 10, 10)
            
            # Add each wrong answer as a separate label
            for wrong in self.wrong_answers:
                answer_label = QLabel(f"{wrong['question']} = {wrong['correct']}   (ai raspuns: {wrong['user_answer']})")
                answer_label.setFont(QFont("Helvetica", 30))
                answer_label.setStyleSheet("color: #5A375A; background: transparent;")
                answer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                wrong_layout.addWidget(answer_label)
            
            wrong_widget.setLayout(wrong_layout)
            scroll_area.setWidget(wrong_widget)
            layout.addWidget(scroll_area)
            layout.addSpacing(10)
        
        layout.addSpacing(20)

        restart_button = QPushButton("Joaca din nou")
        restart_button.setFont(QFont("Helvetica", 24))
        restart_button.setMinimumSize(250, 60)
        restart_button.setStyleSheet("""
            QPushButton {
                background-color: #FFF9FB;
                color: #000000;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FFE6F0;
            }
        """)
        restart_button.clicked.connect(self.restart)
        layout.addWidget(restart_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(15)
        
        quit_button = QPushButton("Inapoi la Meniu")
        quit_button.setFont(QFont("Helvetica", 24))
        quit_button.setMinimumSize(250, 60)
        quit_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #AB47BC;
            }
        """)
        quit_button.clicked.connect(self.quit_to_menu)
        layout.addWidget(quit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        
        exit_button = QPushButton("Inchide Aplicatia")
        exit_button.setFont(QFont("Helvetica", 24))
        exit_button.setMinimumSize(250, 60)
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #E57373;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #EF5350;
            }
        """)
        exit_button.clicked.connect(QApplication.quit)
        layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.main_frame.setLayout(layout)

    # ---------------- Restart ----------------
    def quit_to_menu(self):
        self.timer.stop()
        self.start_menu = StartMenu()
        self.start_menu.show()
        self.close()
    
    def restart(self):
        self.score = 0
        self.current_question = 0
        self.wrong_answers = []
        self.score_label.setText(f"Scor: {self.score}")
        
        # Reset timer
        self.timer.stop()
        self.start_time = None
        self.elapsed_time = 0
        self.timer_label.setText("Timp: 00:00")

        # Rebuild the widgets
        self.build_question_widgets()
        self.new_question()

    # ---------------- Star Animation ----------------
    def spawn_stars(self):
        for _ in range(3):
            x = random.randint(50, self.main_frame.width() - 50) if self.main_frame.width() > 100 else 50
            y = random.randint(50, self.main_frame.height() - 50) if self.main_frame.height() > 100 else 50

            star = QLabel("⭐", self.main_frame)
            star.setFont(QFont("Helvetica", 30))
            star.setStyleSheet("background: transparent;")
            star.move(x, y)
            star.show()

            self.animate_star_label(star, 0)

    def animate_star_label(self, star, step):
        if step > 10:
            star.deleteLater()
            return
        
        current_pos = star.pos()
        star.move(current_pos.x(), current_pos.y() - 8)
        QTimer.singleShot(80, lambda: self.animate_star_label(star, step + 1))


# Gradient widget for background
class GradientWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#F48FB1"))
        gradient.setColorAt(1, QColor("#F06292"))
        painter.fillRect(self.rect(), gradient)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_menu = StartMenu()
    start_menu.show()
    sys.exit(app.exec())
