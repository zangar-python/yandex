from news.models import Blog
from django.contrib.auth.models import User
from .models import Message

def user_liked_blog_send_message(blog:Blog,user:User):
    message = Message.objects.create(
        header=f"{user.username} поставил лайк вашему блогу {blog.header}",
        text=f"Пользователь {user.username} поставил лайк вашему блогу {blog.header}.Всего лайков в этом блоге {blog.likes.count()}",
        from_user=user,
        to_user=blog.author,
    )
    message.save()
    return {
        "message_pk":message.pk,
        "message_header":message.header,
        "to_user":message.to_user.username,
        "to_user_id":message.to_user.id,
        "from_user":message.from_user.username,
        "from_user_id":message.from_user.id,
        "text":message.text
    }
    
def send_followers_message(blog:Blog):
    author = blog.author
    followers = author.follow.followers.all()
    for follower in followers:
        message = Message.objects.create(
            to_user=follower,
            from_user=author,
            header=f"{author.username} опубликовал блог.",
            text=f"{author.username} пользователь на которого вы подписаны,опубликовал новый блог '{blog.header}' "
        )
        message.save()
        print(f"message: {message.header} sended to user {follower.username}")
    print("Message sended")