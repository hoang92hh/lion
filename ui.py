import asyncio
import tkinter as tk
from tkinter import ttk

import config
from excel_manager import open_workbook, load_scenario_data, save_workbook, get_type_scenario,show_scenario
from scenario_runner import run_scenario, stop_scenario




class MainUI:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(
            f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}"
        )
        self.root.minsize(
            config.MIN_WINDOW_WIDTH, config.MIN_WINDOW_HEIGHT
        )

        self.tree = {}
        self.log_text = None
        self.notebook = None  # Khởi tạo thuộc tính lưu Notebook toàn cục
        self.current_scenario_type = config.SCENARIO_IMAGE
        self.create_ui()

# ==========================================================
# UI
    def create_ui(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(button_frame, text="Load", width=12, command=self.load_scenario).pack(side="left", padx=5)
        tk.Button(button_frame, text="Start", width=12, command=self.start_scenario).pack(side="left", padx=5)
        tk.Button(button_frame, text="Stop", width=12, command=self.stop_scenario).pack(side="left", padx=5)
        tk.Button(button_frame, text="Save", width=12, command=self.save_scenario).pack(side="left", padx=5)

        # Sửa thành self.notebook để hàm on_tab_changed có thể truy cập được
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Lắng nghe sự kiện chuyển đổi tab của người dùng
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        self.create_tree(self.notebook, config.SCENARIO_IMAGE)
        self.create_tree(self.notebook, config.SCENARIO_VIDEO)

# ==========================================================
# Tree
    def create_tree(self, notebook, scenario_type):

        frame = ttk.Frame(notebook)
        notebook.add(frame, text=scenario_type.title())
        tree = ttk.Treeview(frame, columns=config.TREE_COLUMNS, show="headings")
        for column in config.TREE_COLUMNS:
            tree.heading(column, text=column)
            tree.column(column, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree[scenario_type] = tree

        if self.log_text is None:
            self.log_text = tk.Text(
                self.root,
                height=config.LOG_HEIGHT,
                font=config.LOG_FONT
            )
            self.log_text.pack(fill="x", padx=10, pady=5)

# ==========================================================
# UI Update

    def update_row_ui(self, scene_id, status, file_name):

        for tree in self.tree.values():

            for item in tree.get_children():

                values = list(
                    tree.item(item, "values")
                )

                if str(values[0]) != str(scene_id):
                    continue

                values[6] = status
                values[8] = file_name

                tree.item(
                    item,
                    values=values
                )

                return

    def log_message(self, message):

        self.log_text.insert(
            "end",
            f"{message}\n"
        )

        if config.LOG_AUTO_SCROLL:
            self.log_text.see("end")

# ==========================================================
# Button
# ==========================================================

    def load_scenario(self):
        try:
            # Luôn đọc chính xác loại scenario đang được chọn hiện tại trên UI
            scenario_type = self.current_scenario_type

            # Lấy đúng Treeview tương ứng với tab hiện tại
            tree = self.tree[scenario_type]

            # Xóa sạch dữ liệu cũ trên bảng hiện tại
            tree.delete(*tree.get_children())

            # Gọi hàm lấy dữ liệu từ excel_manager dựa theo đúng loại tab hiện tại
            sheet = get_type_scenario(scenario_type)
            #scenario_list = load_scenario_data(sheet)
            scenario_list = show_scenario(scenario_type)

            # Nạp dữ liệu vào bảng
            for scene in scenario_list:
                tree.insert(
                    "",
                    "end",
                    values=(
                        scene["scene_id"],
                        scene["template_key"],
                        scene["prompt_core"],
                        scene["character_list"],
                        scene["reference_list"],
                        scene["final_prompt"],
                        scene["status_time"],
                        scene["output_id"],
                        scene["file_name"]
                    )
                )

            self.log_message(f"Load Scenario {scenario_type} Success.")

        except Exception as e:
            self.log_message(f"Load Scenario Failed: {str(e)}")

    def start_scenario(self):
        # 1. Lấy loại scenario hiện tại từ tab đang mở
        scenario_type = self.current_scenario_type

        # 2. Định nghĩa hàm phụ chạy ngầm (Phải viết TRƯỚC khi gọi threading)
        def run_in_thread():
            import asyncio
            asyncio.run(
                run_scenario(
                    self,
                    scenario_type
                )
            )

        # 3. Kích hoạt luồng phụ để chạy hàm vừa định nghĩa ở trên
        import threading
        threading.Thread(target=run_in_thread, daemon=True).start()

    def stop_scenario(self):

        asyncio.run(
            stop_scenario()
        )

        self.log_message(
            "Stop Scenario."
        )

    def save_scenario(self):

        save_workbook()

        self.log_message(
            "Save Workbook Success."
        )

# ==========================================================
# Event Handlers
    def on_tab_changed(self, event):
        """
        Tự động chạy mỗi khi click chuyển đổi Tab trên giao diện.
        Cập nhật lại giá trị biến trạng thái duy nhất của UI.
        """
        current_tab_index = self.notebook.index(self.notebook.select())
        if current_tab_index == 0:
            self.current_scenario_type = config.SCENARIO_IMAGE
        else:
            self.current_scenario_type = config.SCENARIO_VIDEO

        self.log_message(f"Switched to tab: {self.current_scenario_type}")

# ==========================================================
# Main
# ==========================================================
    def run(self):
        self.root.mainloop()
