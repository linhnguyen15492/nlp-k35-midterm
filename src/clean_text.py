import re


def clean_only_chinese_characters(text: str) -> str:
    """
    Hàm lọc và chỉ giữ lại chữ Hán (CJK Characters), loại bỏ chữ Latinh,
    số, dấu câu, và các dòng rác hệ thống. Giữ nguyên cấu trúc dòng văn bản.
    """
    # Định nghĩa dải Unicode của chữ Hán:
    # - \u4e00-\u9fff: CJK Unified Ideographs (Chữ Hán phổ thông)
    # - \u3400-\u4dbf: CJK Unified Ideographs Extension A (Chữ Hán hiếm/cổ)
    # Nếu bạn làm việc với chữ Nôm nặng, có thể mở rộng thêm dải Extension B-G nếu cần.
    cjk_pattern = re.compile(r"[^\u4e00-\u9fff\u3400-\u4dbf]+")

    cleaned_lines = []

    # Xử lý từng dòng để giữ nguyên cấu trúc dòng của bản gốc
    for line in text.splitlines():
        # Loại bỏ các ký tự không phải chữ Hán trong dòng
        # (Thay thế chúng bằng khoảng trắng để tránh dính chữ)
        cleaned_line = cjk_pattern.sub(" ", line).strip()

        # Chỉ giữ lại dòng nếu sau khi làm sạch nó vẫn còn chữ Hán
        if cleaned_line:
            # Thu gọn nhiều khoảng trắng liên tiếp thành 1 khoảng trắng
            cleaned_line = re.sub(r"\s+", " ", cleaned_line)
            cleaned_lines.append(cleaned_line)

    return "\n".join(cleaned_lines)


# --- TEST THỬ VỚI DỮ LIỆU CỦA BẠN ---
if __name__ == "__main__":
    raw_text = """?
卯脆油傳荒唐。杏貽玄鳥生商悟也。
鍾調散合擬奇，可為水火生離如剛
紛紛事拱邏荒歸山歸海恪歌別離
龍龍衛淮南陲 姬姬遙島位傘圓
生張撰沒猥貲。挾鄭役滄踐運艷蟻
雄王都於州峯。意己白鶴合淵泥江，
達滌異滄文郎 紛逝兼部版章拱連
峯州福祿朱薦 認鈴地志術沔山西
定安河內樹台 意州交阯晉玲群傳
新興界墋興宣。武寧省北陽泉省東
太高台省混同 意武定接共边泯
懷雛義九真清越裳異揆治平中州
諒異陸海上游 瞽瀾寧海屬倉廣安
平文九德群韜 床部疆界山川渚詳

===== TRANG MOI =====

--- HVB_004_PDFScan_Trung_Đại Nam quốc sử diễn ca Q1_p0003 ---
?
"""

    print("--- KẾT QUẢ SAU KHI CLEAN ---")
    print(clean_only_chinese_characters(raw_text))
