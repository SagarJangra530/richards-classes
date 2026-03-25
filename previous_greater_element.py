from manim import *

class PreviousGreaterElement(Scene):
    def construct(self):
        arr = [4, 5, 2, 10, 8, 3, 6]
        result = [-1] * len(arr)
        CELL_W = 1.0
        CELL_H = 0.9
        ARR_COLOR   = "#4FC3F7"
        STACK_COLOR = "#FFB74D"
        CUR_COLOR   = "#69F0AE"
        PGE_COLOR   = "#FF6B6B"
        DONE_COLOR  = "#B0BEC5"
        BG_COLOR    = "#0D1117"
        self.camera.background_color = BG_COLOR

        title = Text("Previous Greater Element", font_size=40, color=WHITE, weight=BOLD)
        subtitle = Text("Using a Monotonic Stack  |  O(n) Time · O(n) Space", font_size=22, color=GREY_B)
        title_grp = VGroup(title, subtitle).arrange(DOWN, buff=0.15)
        title_grp.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP*0.2), run_time=0.7)
        self.wait(0.4)

        prob = Text("For every element, find the nearest element to its LEFT that is GREATER.", font_size=21, color="#CFD8DC")
        prob.next_to(title_grp, DOWN, buff=0.25)
        self.play(FadeIn(prob), run_time=0.8)
        self.wait(0.5)

        def make_cell(val, color=ARR_COLOR, idx=None):
            rect = RoundedRectangle(width=CELL_W, height=CELL_H, corner_radius=0.12,
                                    fill_color=color, fill_opacity=0.85,
                                    stroke_color=WHITE, stroke_width=1.5)
            num = Text(str(val), font_size=32, color=WHITE, weight=BOLD)
            num.move_to(rect)
            grp = VGroup(rect, num)
            if idx is not None:
                idx_lbl = Text(str(idx), font_size=16, color=GREY_B)
                idx_lbl.next_to(rect, DOWN, buff=0.06)
                grp.add(idx_lbl)
            return grp

        n = len(arr)
        arr_label = Text("Input Array:", font_size=24, color=GREY_A, weight=BOLD)
        arr_label.move_to([-4.5, 0.8, 0])
        cells = VGroup(*[make_cell(arr[i], ARR_COLOR, i) for i in range(n)])
        cells.arrange(RIGHT, buff=0.18)
        cells.move_to([0.5, 0.8, 0])
        self.play(FadeIn(arr_label), LaggedStart(*[FadeIn(c, shift=DOWN*0.3) for c in cells], lag_ratio=0.12), run_time=1.4)
        self.wait(0.3)

        res_label = Text("Result:", font_size=24, color=GREY_A, weight=BOLD)
        res_label.move_to([-4.5, -0.5, 0])
        res_cells = VGroup(*[make_cell("?", DONE_COLOR, i) for i in range(n)])
        res_cells.arrange(RIGHT, buff=0.18)
        res_cells.move_to([0.5, -0.5, 0])
        self.play(FadeIn(res_label), LaggedStart(*[FadeIn(c, shift=DOWN*0.2) for c in res_cells], lag_ratio=0.12), run_time=1.2)
        self.wait(0.3)

        stack_label = Text("Stack (indices):", font_size=22, color=GREY_A, weight=BOLD)
        stack_label.move_to([-4.8, -2.1, 0])
        stack_area = RoundedRectangle(width=6.5, height=1.1, corner_radius=0.12,
                                      fill_color="#1E272E", fill_opacity=1,
                                      stroke_color="#546E7A", stroke_width=1.5)
        stack_area.move_to([0.5, -2.1, 0])
        self.play(FadeIn(stack_label), Create(stack_area), run_time=0.7)

        stack_cells_vg = VGroup()

        def legend_dot(color, label):
            d = Dot(color=color, radius=0.12)
            t = Text(label, font_size=18, color=GREY_B)
            return VGroup(d, t).arrange(RIGHT, buff=0.15)

        leg = VGroup(
            legend_dot(CUR_COLOR,  "Current"),
            legend_dot(STACK_COLOR,"In Stack"),
            legend_dot(PGE_COLOR,  "PGE Found"),
            legend_dot(DONE_COLOR, "Processed"),
        ).arrange(RIGHT, buff=0.55)
        leg.to_edge(DOWN, buff=0.22)
        self.play(FadeIn(leg), run_time=0.6)

        info_box = RoundedRectangle(width=9, height=0.7, corner_radius=0.1,
                                    fill_color="#1A237E", fill_opacity=0.7,
                                    stroke_color="#3F51B5", stroke_width=1)
        info_box.next_to(res_cells, DOWN, buff=0.35)
        info_text = Text("", font_size=20, color=WHITE)
        info_text.move_to(info_box)
        self.play(FadeIn(info_box), run_time=0.4)

        def update_info(msg, color=WHITE):
            nonlocal info_text
            new_t = Text(msg, font_size=19, color=color)
            new_t.move_to(info_box)
            self.play(Transform(info_text, new_t), run_time=0.35)

        stack = []

        def rebuild_stack_visual():
            nonlocal stack_cells_vg
            self.remove(stack_cells_vg)
            if not stack:
                stack_cells_vg = VGroup()
                return
            new_cells = VGroup()
            for idx_val in stack:
                c = make_cell(f"{idx_val}({arr[idx_val]})", STACK_COLOR)
                new_cells.add(c)
            new_cells.arrange(RIGHT, buff=0.15)
            new_cells.move_to(stack_area)
            stack_cells_vg = new_cells
            self.play(FadeIn(stack_cells_vg, shift=UP*0.1), run_time=0.35)

        def update_result_cell(i, val):
            col = PGE_COLOR if val != -1 else "#78909C"
            new_c = make_cell(str(val), col, i)
            new_c.move_to(res_cells[i])
            self.play(Transform(res_cells[i], new_c), run_time=0.4)

        self.wait(0.3)

        for i in range(n):
            self.play(cells[i][0].animate.set_fill(CUR_COLOR), run_time=0.3)
            update_info(f"i={i}  arr[i]={arr[i]}  ->  pop stack while top <= {arr[i]}")

            while stack and arr[stack[-1]] <= arr[i]:
                popped = stack.pop()
                self.play(cells[popped][0].animate.set_fill(DONE_COLOR), run_time=0.25)

            rebuild_stack_visual()

            if stack:
                pge_idx = stack[-1]
                result[i] = arr[pge_idx]
                self.play(cells[pge_idx][0].animate.set_fill(PGE_COLOR), run_time=0.3)
                arrow = Arrow(
                    start=cells[pge_idx].get_top() + UP*0.05,
                    end=cells[i].get_top() + UP*0.05,
                    color=PGE_COLOR, stroke_width=3,
                    tip_length=0.2, buff=0.05,
                    path_arc=-PI/3
                )
                self.play(Create(arrow), run_time=0.45)
                update_info(f"PGE of arr[{i}]={arr[i]}  is  arr[{pge_idx}]={arr[pge_idx]}", color=PGE_COLOR)
                self.wait(0.5)
                self.play(FadeOut(arrow), run_time=0.3)
                self.play(cells[pge_idx][0].animate.set_fill(STACK_COLOR), run_time=0.2)
            else:
                result[i] = -1
                update_info(f"Stack empty -> PGE of arr[{i}]={arr[i]}  is  -1", color="#78909C")
                self.wait(0.5)

            update_result_cell(i, result[i])
            stack.append(i)
            rebuild_stack_visual()
            self.play(cells[i][0].animate.set_fill(STACK_COLOR), run_time=0.2)
            self.wait(0.15)

        update_info("Algorithm complete!  All elements processed", color=CUR_COLOR)
        for idx_val in stack:
            self.play(cells[idx_val][0].animate.set_fill(DONE_COLOR), run_time=0.2)
        self.wait(0.4)

        final_box = RoundedRectangle(width=8, height=0.65, corner_radius=0.1,
                                     fill_color="#1B5E20", fill_opacity=0.85,
                                     stroke_color="#66BB6A", stroke_width=2)
        final_box.next_to(res_cells, DOWN, buff=0.6)
        res_vals = "  ".join(str(v) for v in result)
        final_txt = Text(f"Result: [ {res_vals} ]", font_size=22, color="#A5D6A7", weight=BOLD)
        final_txt.move_to(final_box)
        self.play(FadeIn(final_box), Write(final_txt), run_time=0.9)
        self.wait(0.5)

        complex_txt = Text("Time Complexity: O(n)   |   Space Complexity: O(n)", font_size=20, color="#FFD54F")
        complex_txt.next_to(final_box, DOWN, buff=0.2)
        self.play(FadeIn(complex_txt, shift=UP*0.15), run_time=0.7)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.2)
        outro = Text("Previous Greater Element — Done!", font_size=38, color=CUR_COLOR, weight=BOLD)
        self.play(Write(outro), run_time=1.0)
        self.wait(1.5)
