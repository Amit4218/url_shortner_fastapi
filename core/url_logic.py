from datetime import datetime, timedelta

from fastapi import HTTPException, Request
from sqlalchemy import desc, func, select

from config import Session
from models import NotRegisteredUrls, UrlLogs, Urls, User


def save_url(db: Session, original_url: str, id: str, unique_url: str):
    url = Urls(original_url=original_url, short_url=unique_url, user_id=id)

    db.add(url)
    db.commit()
    db.refresh(url)

    return {"url": unique_url}


def get_redirect_url(db: Session, url: str, request_obj: Request):
    short_url = url.split("/")[-1]

    existng_url = db.query(Urls).filter(Urls.short_url == short_url).first()

    if not existng_url:
        raise HTTPException(status_code=404, detail="url not found!")

    existng_url.total_requests += 1

    url_request_metadata = UrlLogs(
        requested_url=str(request_obj.url),
        requested_by=request_obj.client.host if request_obj.client else "unknown",
        url_id=existng_url.id,
    )

    db.add(url_request_metadata)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return existng_url.original_url


def get_url_metadata(db: Session, user_id: str, logs_limit: int = 10):
    urls = db.execute(select(Urls).where(Urls.user_id == user_id)).scalars().all()

    data = {}

    for url in urls:
        logs = (
            db.execute(
                select(UrlLogs)
                .where(UrlLogs.url_id == url.id)
                .order_by(desc(UrlLogs.requested_at))
                .limit(logs_limit)
            )
            .scalars()
            .all()
        )

        data[str(url.id)] = {
            "original_url": url.original_url,
            "short_url": url.short_url,
            "total_requests": url.total_requests,
            "created_at": url.created_at,
            "logs": [
                {
                    "requested_url": log.requested_url,
                    "requested_by": log.requested_by,
                    "requested_at": log.requested_at,
                }
                for log in logs
            ],
        }

    return data


def save_temp_url(db: Session, original_url: str, unique_url: str):
    url = NotRegisteredUrls(original_url=original_url, short_url=unique_url)

    db.add(url)
    db.commit()
    db.refresh(url)

    return {"url": unique_url}


def get_temp_url_redirect(db: Session, url: str):
    short_url = url.split("/")[-1]

    existng_url = (
        db.query(NotRegisteredUrls)
        .filter(NotRegisteredUrls.short_url == short_url)
        .first()
    )

    if not existng_url:
        raise HTTPException(status_code=404, detail="url not found!")

    existng_url.total_requests += 1

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return existng_url.original_url


def get_current_stats(db: Session) -> dict:
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)

    total_user_count = db.query(User).count()
    urls_count = db.query(Urls).count()
    temp_urls_count = db.query(NotRegisteredUrls).count()

    urls_last_10_min = (
        db.query(func.count(Urls.id))
        .filter(Urls.created_at >= ten_minutes_ago)
        .scalar()
    )

    temp_urls_last_10_min = (
        db.query(func.count(NotRegisteredUrls.id))
        .filter(NotRegisteredUrls.created_at >= ten_minutes_ago)
        .scalar()
    )

    total_urls_count = urls_count + temp_urls_count

    url_created_last_10_minutes_ago = urls_last_10_min + temp_urls_last_10_min

    data = {
        "total_users": total_user_count,
        "total_urls": total_urls_count,
        "url_created_10_minutes_ago": url_created_last_10_minutes_ago,
    }

    return data


# def count_short_links_since(db: Session, since: datetime) -> int:
#     return (
#         db.query(func.count(Urls.id)).filter(Urls.created_at >= since).scalar()
#         + db.query(func.count(NotRegisteredUser.id))
#         .filter(NotRegisteredUser.created_at >= since)
#         .scalar()
#     )
