# --------------------------------------------------------------------------
# QnA schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class FileSchema(BaseModel):
    id: int = Field(..., title="File ID", description="파일의 고유 식별자입니다.")
    type: str = Field(..., title="File Type", description="파일의 유형입니다.")
    url: str = Field(..., title="File Name", description="파일의 이름입니다.")  # TODO : url로 수정할 것


class CommentSchema(BaseModel):
    id: int = Field(..., title="Comment ID", description="댓글의 고유 식별자입니다.")
    contentId: int = Field(
        ..., title="Content ID", description="컨텐츠의 고유 식별자입니다."
    )
    writerId: UUID = Field(
        ..., title="Writer ID", description="작성자의 고유 식별자입니다."
    )
    description: str = Field(
        ..., title="Comment Description", description="댓글 내용입니다."
    )
    remove: bool = Field(..., title="Remove Flag", description="댓글 삭제 여부입니다.")

    class ConfigDict:
        from_attributes = True


class QnASchema(BaseModel):
    id: int = Field(..., title="QnA ID", description="QnA의 고유 식별자입니다.")
    writerId: UUID = Field(
        ..., title="Writer ID", description="작성자의 고유 식별자입니다."
    )
    categoryId: int = Field(
        ..., title="Category ID", description="카테고리의 고유 식별자입니다."
    )
    title: str = Field(..., title="Title", description="QnA의 제목입니다.")
    description: str = Field(..., title="Description", description="QnA의 내용입니다.")
    viewCount: int = Field(..., title="View Count", description="조회수입니다.")
    createdAt: datetime = Field(..., title="Created At", description="생성 날짜입니다.")
    modifiedAt: datetime = Field(
        ..., title="Modified At", description="수정 날짜입니다."
    )
    remove: bool = Field(..., title="Remove Flag", description="삭제 여부입니다.")
    file: List[FileSchema] = Field(
        None, title="Files", description="첨부된 파일 목록입니다."
    )
    comments: List[CommentSchema] = Field(
        None, title="Comments", description="댓글 목록입니다."
    )
    likes: int = Field(..., title="Likes", description="좋아요 수입니다.")

    class ConfigDict:
        from_attributes = True


class QnACreate(BaseModel):
    writerId: UUID = Field(..., title="Writer ID", description="작성자의 고유 식별자입니다.")
    categoryId: int = Field(..., title="Category ID", description="카테고리의 고유 식별자입니다.")
    title: str = Field(..., title="Title", description="QnA의 제목입니다.")
    description: str = Field(..., title="Description", description="QnA의 내용입니다.")
    file: List[FileSchema] = Field(..., title="Files", description="첨부된 파일 목록입니다.")


class QnAUpdate(BaseModel):
    categoryId: Optional[int] = Field(None, title="Category ID", description="카테고리의 고유 식별자입니다.")
    title: Optional[str] = Field(None, title="Title", description="QnA의 제목입니다.")
    description: Optional[str] = Field(None, title="Description", description="QnA의 내용입니다.")
    file: Optional[List[FileSchema]] = Field(None, title="Files", description="첨부된 파일 목록입니다.")
