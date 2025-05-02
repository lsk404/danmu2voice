from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, 
                           QWidget, QSystemTrayIcon, QMenu, QStyle)
from PyQt5.QtCore import Qt,QTimer,QRect,QMargins
from PyQt5.QtGui import QIcon,QFontMetrics,QFont
import sys

class DraggableWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # 设置窗口名称和标题
        self.setWindowTitle("text_show")
        
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # 创建托盘菜单
        self.create_tray_menu()
        
        # 窗口初始化设置
        self.init_ui()
        
    def create_tray_menu(self):
        """创建托盘右键菜单"""
        tray_menu = QMenu()
        
        # 显示/隐藏窗口选项
        self.toggle_action = tray_menu.addAction("隐藏窗口")
        self.toggle_action.triggered.connect(self.toggle_window)
        
        # 分隔线
        tray_menu.addSeparator()
        
        # 退出选项
        quit_action = tray_menu.addAction("退出")
        quit_action.triggered.connect(sys.exit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # 点击托盘图标恢复窗口
        self.tray_icon.activated.connect(self.tray_icon_clicked)
        
    def init_ui(self):
        # 主布局
        layout = QVBoxLayout()
        
        # 内容标签
        self.label = QLabel("窗口内容区域", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.setLayout(layout)


        # 设置初始字体和行间距
        self.initial_font_size = 32
        font = QFont()
        font.setPointSize(self.initial_font_size)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.label.setFont(font)
        
        layout.addWidget(self.label)
        self.setLayout(layout)
        
       # 通过样式表设置透明背景
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 启用透明背景
        # self.setStyleSheet("background: transparent;")  # 设置样式表

        # 固定窗口大小并设置边距
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus)
        self.setGeometry(100, 100, 600, 400)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = None
            event.accept()
    def toggle_window(self):
        """切换窗口显示/隐藏状态"""
        if self.isVisible():
            self.hide()
            self.toggle_action.setText("显示窗口")
            self.tray_icon.showMessage("提示", "程序已最小化到系统托盘")
        else:
            self.showNormal()
            self.activateWindow()
            self.toggle_action.setText("隐藏窗口")
        
    def tray_icon_clicked(self, reason):
        """托盘图标点击事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_window()
            
    def closeEvent(self, event):
        """重写关闭事件，隐藏到托盘而不是退出"""
        self.hide()
        self.toggle_action.setText("显示窗口")
        event.ignore()

    def update_text(self, new_text):
        """更新文本：严格优先换行，换行后仍无法显示才缩小字体"""
        if not new_text:
            return
        
        # 1. 初始化设置
        font = self.label.font()
        font.setPointSize(self.initial_font_size)
        self.label.setFont(font)
        self.label.setText(new_text)
        self.label.setWordWrap(True)  # 强制启用换行
        self.label.setAlignment(Qt.AlignCenter)
        
        # 2. 计算精确可用空间（考虑所有边距）
        margins = self.layout().contentsMargins() if self.layout() else QMargins(10, 10, 10, 10)
        label_margins = self.label.contentsMargins()
        
        available_width = max(10, self.width() - margins.left() - margins.right() 
                            - label_margins.left() - label_margins.right())
        available_height = max(10, self.height() - margins.top() - margins.bottom() 
                        - label_margins.top() - label_margins.bottom())
        
        # 3. 分阶段检查：严格先换行后缩小
        needs_shrink = False
        current_font = font
        fm = QFontMetrics(current_font)
        
        # 阶段1：检查在初始字体下，仅靠换行是否能完全显示
        text_rect = fm.boundingRect(
            QRect(0, 0, available_width, 0),
            Qt.TextWordWrap | Qt.TextIncludeTrailingSpaces,
            new_text
        )
        
        # 判断标准：换行后的高度是否超出可用高度
        if text_rect.height() > available_height:
            needs_shrink = True
        
        # 阶段2：只有当换行无法完全显示时才缩小字体
        if needs_shrink:
            min_font_size = 6  # 最小字体限制
            while current_font.pointSize() > min_font_size:
                # 先缩小字体
                current_font.setPointSize(current_font.pointSize() - 1)
                self.label.setFont(current_font)
                fm = QFontMetrics(current_font)
                
                # 检查缩小后的字体是否可以通过换行完全显示
                text_rect = fm.boundingRect(
                    QRect(0, 0, available_width, 0),
                    Qt.TextWordWrap | Qt.TextIncludeTrailingSpaces,
                    new_text
                )
                
                # 如果换行后能完整显示，立即停止缩小
                if text_rect.height() <= available_height:
                    break
        
        # 4. 最终确认（防止极端情况）
        final_fm = QFontMetrics(self.label.font())
        final_rect = final_fm.boundingRect(
            QRect(0, 0, available_width, available_height),
            Qt.TextWordWrap | Qt.AlignCenter | Qt.TextIncludeTrailingSpaces,
            new_text
        )
        
        # 如果仍然无法显示，使用省略号
        if final_rect.height() > available_height:
            elided_lines = available_height // final_fm.lineSpacing()
            elided_text = self._get_elided_text(new_text, final_fm, available_width, elided_lines)
            self.label.setText(elided_text)

    def _get_elided_text(self, text, font_metrics, width, max_lines):
        """生成带省略号的多行文本"""
        lines = []
        current_line = ""
        
        for word in text.split():
            test_line = f"{current_line} {word}".strip()
            if font_metrics.horizontalAdvance(test_line) <= width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
                if len(lines) >= max_lines:
                    break
        
        if current_line and len(lines) < max_lines:
            lines.append(current_line)
        
        if len(lines) >= max_lines:
            last_line = lines[max_lines-1]
            if font_metrics.horizontalAdvance(last_line) > width:
                lines[max_lines-1] = font_metrics.elidedText(last_line, Qt.ElideRight, width)
            return "\n".join(lines[:max_lines])
        return "\n".join(lines)

def change_window_text(window, text):
    
    window.update_text(text)

if __name__ == "__main__":
    app = QApplication([])
    
    # 确保应用程序有系统托盘支持
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("系统不支持托盘图标!")
        exit(1)
    
    # 设置应用程序图标（可选）
    app.setWindowIcon(QIcon.fromTheme("accessories-text-editor"))
    
    window = DraggableWindow()

    # 关键设置：强制使用OpenGL渲染
    window.setAttribute(Qt.WA_PaintOnScreen, True)  # 直接绘制到屏幕（避免缓冲）
    window.setAttribute(Qt.WA_NativeWindow, True)   # 确保使用原生窗口句柄
    # window.setAttribute(Qt.WA_NoSystemBackground, True)  # 禁用系统背景
    
    window.show()
    def start_text_loop(window, test_texts, index=0):
        # 切换到当前文本
        change_window_text(window, test_texts[index])
        
        # 在当前文本显示后设置定时器触发下一个文本
        next_index = (index + 1) % len(test_texts)  # 确保循环
        QTimer.singleShot(2000, lambda: start_text_loop(window, test_texts, next_index))
    # 测试更极端的文本
    test_texts = [
        "短文本",
        "中等长度文本，测试自动换行功能",
        "这是一个非常非常非常非常非常非常非常非常非常长的文本，它会自动换行并调整大小以适应窗口",
        "超长文本测试：" + "很长很长的文本，" * 20,
        "回到短文本",
        "测试英文abcd,ln(sec+tan)+C"
    ]
    start_text_loop(window, test_texts)
    
    app.exec_()