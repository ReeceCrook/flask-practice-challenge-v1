from config import app, api
from models import Post, Comment
from flask_restful import Resource

# create routes here:
class SortedPosts(Resource):
  def get(self):
    posts = Post.query.all()
    sorted_posts = sorted(posts, key=lambda x: x.title)
    
    return [post.to_dict() for post in sorted_posts]
  
class PostsByAuthor(Resource):
  def get(self, author_name):
    posts = Post.query.filter(Post.author == author_name).all()
    return [post.to_dict() for post in posts]
  
class SearchPosts(Resource):
  def get(self, title):
    posts = Post.query.filter(Post.title.ilike(title)).all()
    return [post.to_dict() for post in posts]

class PostsOrderedByComments(Resource):
  def get(self):
    posts = Post.query.all()
    sorted_posts = sorted(posts, key=lambda x: len(x.comments), reverse=True)
    return [post.to_dict() for post in sorted_posts]
  
class MostPopularCommentor(Resource):
  def get(self):
    comments = Comment.query.all()
    commenters = {}
    for comment in comments:
      if comment.commenter not in commenters:
        commenters[comment.commenter] = 1
      else:
        commenters[comment.commenter] += 1
        
    top_commenter = []
    highest_comments = max(commenters.values())
    for commenter in commenters:
      if commenters[commenter] == highest_comments:
        top_commenter.append({'commenter': commenter, 'ammount_of_comments': commenters[commenter]})
    
    return [commenter for commenter in top_commenter]

  


api.add_resource(SortedPosts, "/api/sorted_posts/")
api.add_resource(PostsByAuthor, "/api/posts_by_author/<string:author_name>")
api.add_resource(SearchPosts, "/api/search_posts/<string:title>")
api.add_resource(PostsOrderedByComments, "/api/posts_ordered_by_comments/")
api.add_resource(MostPopularCommentor, "/api/most_popular_commenter/")

if __name__ == "__main__":
  app.run(port=5555, debug=True)