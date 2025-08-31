from news.models import Blog,Comment
from news.comments.serializer import CommentSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
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
    return

def send_comment(comment_serializer:CommentSerializer):
    comment : Comment = get_object_or_404(Comment,id=comment_serializer['id'])
    comment_user:User = comment.user
    author:User = comment.to_blog.author
    Message.objects.create(
        to_user=author,
        from_user=comment_user,
        header=f"{comment_user.username} коментировал ваш блог",
        text = f"{comment_user.username} коментировал ваш блог {comment.to_blog.header}.'{comment.text}'"
    )
    print("message sended")
    return

def send_comment_like(comment:Comment,user:User):
    comment_user = comment.user
    Message.objects.create(
        to_user=comment_user,
        from_user=user,
        header=f"{user.username} Поставил лайк вашему комменту",
        text = f"{user.username} поставил лайк вашему комментарию {comment.text} под блогом {comment.to_blog.header}"
    )
    return