# --------------------------------------------------------------------------
# 페이지네이션 관련 헬퍼 함수 및 스키마들을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel, Field, AnyHttpUrl
from fastapi import Request

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    count: int = Field(..., title="Count", description="불러온 아이템 전체 개수를 나타냅니다.")
    next: Optional[AnyHttpUrl] = Field(
        None,
        title="Next",
        description="데이터를 불러올 다음 페이지의 URL을 나타냅니다.",
    )
    previous: Optional[AnyHttpUrl] = Field(
        None,
        title="Previous",
        description="데이터를 불러왔던 이전 페이지의 URL을 나타냅니다.",
    )
    results: List[T] = Field(
        ...,
        title="Results",
        description="불러온 아이템들의 정보들을 리스트로 나타냅니다.",
    )


class Paginator:
    def __init__(self, data: List[T], page: int, per_page: int, request: Request):
        self.data = data
        self.page = page
        self.page_size = per_page
        self.limit = per_page
        self.offset = (page - 1) * per_page
        self.request = request
        self.number_of_pages = self._get_number_of_pages(len(data))

    def _get_next_page(self) -> Optional[str]:
        if self.page >= self.number_of_pages:
            return None
        url = self.request.url.include_query_params(page=self.page + 1)
        return str(url)

    def _get_previous_page(self) -> Optional[str]:
        if self.page == 1:
            return None
        url = self.request.url.include_query_params(page=self.page - 1)
        return str(url)

    def get_response(self) -> dict:
        paginated_data = self.data[self.offset:self.offset + self.limit]
        return {
            "count": len(self.data),
            "next": self._get_next_page(),
            "previous": self._get_previous_page(),
            "results": paginated_data,
        }

    def _get_number_of_pages(self, count: int) -> int:
        rest = count % self.page_size
        quotient = count // self.page_size
        return quotient if not rest else quotient + 1


def paginate(data: List[T], page: int, page_size: int, request: Request) -> dict:
    paginator = Paginator(data, page, page_size, request)
    return paginator.get_response()
