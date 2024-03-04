from fastapi import Depends, FastAPI, HTTPException
import uvicorn

from database import engine,SessionLocal
from models import Base, User
from schemas import UserSchema, UserUpdateSchema
from sqlalchemy.orm import Session
app = FastAPI()
Base.metadata.create_all(bind=engine)
def get_db():
    try :
        db = SessionLocal()
        yield db
    finally:
        db.close()
@app.post("/addUser")
async def add_user(req: UserSchema, db: Session = Depends(get_db)):
    user = User(name=req.name, email=req.email, nickname=req.nickname)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"status_code": 200, "message": "Successfully added user"}

@app.get("/Users/{user_id}")
async def getUser(user_id:int,db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user :
        return user
    return HTTPException(status_code=404,detail="User not found")
@app.get("/AllUsers")
async def allUsers(db:Session=Depends(get_db)):
    users = db.query(User).all()
    return users

from fastapi import HTTPException

@app.delete("/Users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/Users/{user_id}")
async def edit_user(user_id: int, user_update_data: UserUpdateSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_update_data.name
    user.email = user_update_data.email
    user.nickname = user_update_data.nickname
    db.commit()
    return {"message": "User updated successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)