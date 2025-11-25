import numpy as np
# import json  <-- Bỏ dòng này vì không đọc file local nữa
from logic.ProjectInfo import ProjectInfo
from logic.UserInfo import UserInfo
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
import src.data.fb as fb  # <-- THÊM: Import file fb để lấy dữ liệu


class Suggestion:
    def load_data(self) -> List[ProjectInfo]:
        data = fb.get_all_projects()
        if not data:
            return []
        try:
            return [ProjectInfo(**item) for item in data]
        except Exception as e:
            return []

    def _combine_fields_to_doc(self, obj: UserInfo | ProjectInfo) -> str:
        all_tags = []
        all_tags.extend(obj.skills)
        all_tags.extend(obj.major)
        all_tags.extend(obj.interests)
        return " ".join([tag.lower() for tag in all_tags])

    def __init__(self):
        self.projects = self.load_data()
        project_docs = [self._combine_fields_to_doc(proj) for proj in self.projects]

        # Thêm kiểm tra để tránh lỗi empty vocabulary nếu project_docs rỗng
        if not project_docs:
            print("No projects loaded. Suggestion engine is empty.")
            self.project_vectors = np.array([])
            # Tạo vectorizer rỗng hoặc dummy để không crash các hàm sau
            try:
                self.vectorizer = CountVectorizer(binary=True).fit(["dummy data"])
            except:
                pass
            return

        self.vectorizer = CountVectorizer(binary=True).fit(project_docs)
        self.project_vectors = self.vectorizer.transform(
            project_docs)  # Dùng transform thay vì fit_transform để đồng bộ
        print(f"Successfully loaded and vectorized {len(self.projects)} projects.")
        print(f"Vocabulary size (total unique tags): {len(self.vectorizer.get_feature_names_out())}")

    def embed_object(self, obj: UserInfo | ProjectInfo) -> np.ndarray:
        doc = self._combine_fields_to_doc(obj)
        vector = self.vectorizer.transform([doc])
        return vector

    def ProjectSuggestList(self, user: UserInfo, top_n: int = 5) -> List[ProjectInfo]:
        if self.project_vectors.size == 0:
            print("No projects available for suggestion.")
            return []

        user_vector = self.embed_object(user)
        similarities = cosine_similarity(user_vector, self.project_vectors).flatten()
        temp_matches = []
        for i, score in enumerate(similarities):
            temp_matches.append((score, self.projects[i]))
        temp_matches.sort(key=lambda x: x[0], reverse=True)
        top_10_matches = temp_matches[:10]
        temp_easiness_sort = []
        for score, proj in top_10_matches:
            temp_easiness_sort.append((len(proj.skills), proj.estimated_hours, proj))
        sorted_by_easiness = sorted(temp_easiness_sort, key=lambda x: (x[0], x[1]))
        suggested_projects = [proj for _, _, proj in sorted_by_easiness]
        return suggested_projects