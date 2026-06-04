import flet as ft
import json
import os

DATA_FILE = "tracker_data.json"
DEFAULT_DATA = {
    "balance": 0,
    "earning": {"10": ["Сделать зарядку", "Выпить воды"], "15": ["Прочитать 20 страниц"]},
    "spending": {"20": ["Посмотреть сериал"], "30": ["Купить вкусняшку"]}
}

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except Exception: pass
    return DEFAULT_DATA.copy()

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception: pass

def main(page: ft.Page):
    page.title = "Трекер Баллов"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.window_min_width = 350
    data = load_data()

    balance_text = ft.Text(f"{data['balance']} 🪙", size=40, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN)

    def build_grid(items_dict, is_earning):
        grid = ft.GridView(expand=True, runs_count=5, max_extent=160, child_aspect_ratio=1.0, spacing=10, run_spacing=10)
        for pts in sorted(items_dict.keys(), key=int):
            color = ft.colors.GREEN_100 if is_earning else ft.colors.RED_100
            text_color = ft.colors.GREEN_900 if is_earning else ft.colors.RED_900
            for task in items_dict[pts]:
                card = ft.GestureDetector(
                    content=ft.Card(content=ft.Container(
                        content=ft.Column([
                            ft.Row([ft.Icon(ft.icons.STAR, color=ft.colors.AMBER, size=20), ft.Text(f"{pts} б.", weight=ft.FontWeight.BOLD, color=text_color)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(task, size=14, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=10, bgcolor=color, border_radius=12), elevation=2),
                    on_tap=lambda e, p=int(pts), name=task, earn=is_earning: handle_tap(p, name, earn)
                )
                grid.controls.append(card)
        return grid

    def handle_tap(points, name, is_earning):
        if is_earning:
            data["balance"] += points
        else:
            if data["balance"] >= points: data["balance"] -= points
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"⚠️ Нужно {points}, есть {data['balance']}", color=ft.colors.WHITE), bgcolor=ft.colors.ORANGE)
                page.snack_bar.open = True
                page.update()
                return
        save_data(data)
        balance_text.value = f"{data['balance']} 🪙"
        page.snack_bar = ft.SnackBar(content=ft.Text(f"{'✅ +' if is_earning else '💸 -'}{points}: {name}", color=ft.colors.WHITE), bgcolor=ft.colors.GREEN if is_earning else ft.colors.RED)
        page.snack_bar.open = True
        page.update()

    tabs = ft.Tabs(selected_index=0, animation_duration=300, tabs=[
        ft.Tab(text="📈 Доход", content=build_grid(data["earning"], True)),
        ft.Tab(text="📉 Траты", content=build_grid(data["spending"], False)),
    ])

    page.appbar = ft.AppBar(title=ft.Text("Мой Трекер", weight=ft.FontWeight.BOLD), center_title=True, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE)
    page.add(
        ft.Container(content=ft.Column([ft.Text("Баланс:", size=16, color=ft.colors.GREY_700), balance_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=15, bgcolor=ft.colors.BLUE_50, border_radius=15, margin=ft.margin.only(bottom=15)),
        ft.Container(content=tabs, expand=True)
    )

if __name__ == "__main__":
    ft.app(target=main)