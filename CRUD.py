from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime


class BlogCompleto:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Blog"]
        self.users = self.db["users"]
        self.articles = self.db["articles"]
        self.tags = self.db["tags"]
        self.categories = self.db["categories"]
        self.comments = self.db["comments"]

    # usuarios
    def crear_usuario(self, nombre, email):
        usuario = {
            "name": nombre,
            "email": email,
            "created_at": datetime.now()
        }
        return self.users.insert_one(usuario).inserted_id

    def obtener_usuarios(self):
        return list(self.users.find())

    def actualizar_usuario(self, user_id, nuevos_datos):
        return self.users.update_one({"_id": ObjectId(user_id)}, {"$set": nuevos_datos})

    def eliminar_usuario(self, user_id):
        return self.users.delete_one({"_id": ObjectId(user_id)})

    def buscar_usuarios(self, filtro):
        """Buscar usuarios por nombre, email, etc."""
        return list(self.users.find(filtro))

    def contar_usuarios(self, filtro=None):
        """Contar usuarios (con o sin filtro)"""
        return self.users.count_documents(filtro or {})

    ##
    def crear_articulo(self, titulo, texto, autor_id, tags=None, categorias=None):
        articulo = {
            "title": titulo,
            "text": texto,
            "date": datetime.now(),
            "author_id": ObjectId(autor_id),
            "tags": [ObjectId(t) for t in (tags or [])],
            "categories": [ObjectId(c) for c in (categorias or [])]
        }
        return self.articles.insert_one(articulo).inserted_id

    def obtener_articulos(self):
        return list(self.articles.find())

    def actualizar_articulo(self, articulo_id, nuevos_datos):
        return self.articles.update_one({"_id": ObjectId(articulo_id)}, {"$set": nuevos_datos})

    def eliminar_articulo(self, articulo_id):
        return self.articles.delete_one({"_id": ObjectId(articulo_id)})

    def buscar_articulos(self, filtro):
        """Buscar artículos por título, texto, autor, etc."""
        return list(self.articles.find(filtro))

    def contar_articulos(self, filtro=None):
        """Contar artículos (con o sin filtro)"""
        return self.articles.count_documents(filtro or {})

    ##
    def crear_tag(self, nombre, url):
        tag = {
            "name": nombre,
            "url": url,
            "created_at": datetime.now()
        }
        return self.tags.insert_one(tag).inserted_id

    def obtener_tags(self):
        return list(self.tags.find())

    def actualizar_tag(self, tag_id, nuevos_datos):
        return self.tags.update_one({"_id": ObjectId(tag_id)}, {"$set": nuevos_datos})

    def eliminar_tag(self, tag_id):
        return self.tags.delete_one({"_id": ObjectId(tag_id)})

    def buscar_tags(self, filtro):
        """Buscar tags por nombre, url, etc."""
        return list(self.tags.find(filtro))

    def contar_tags(self, filtro=None):
        """Contar tags (con o sin filtro)"""
        return self.tags.count_documents(filtro or {})

    ##
    def crear_categoria(self, nombre, url):
        categoria = {
            "name": nombre,
            "url": url,
            "created_at": datetime.now()
        }
        return self.categories.insert_one(categoria).inserted_id

    def obtener_categorias(self):
        return list(self.categories.find())

    def actualizar_categoria(self, categoria_id, nuevos_datos):
        return self.categories.update_one({"_id": ObjectId(categoria_id)}, {"$set": nuevos_datos})

    def eliminar_categoria(self, categoria_id):
        return self.categories.delete_one({"_id": ObjectId(categoria_id)})

    def buscar_categorias(self, filtro):
        """Buscar categorías por nombre, url, etc."""
        return list(self.categories.find(filtro))

    def contar_categorias(self, filtro=None):
        """Contar categorías (con o sin filtro)"""
        return self.categories.count_documents(filtro or {})

    ##
    def crear_comentario(self, articulo_id, autor_id, texto):
        comentario = {
            "article_id": ObjectId(articulo_id),
            "author_id": ObjectId(autor_id),
            "text": texto,
            "date": datetime.now()
        }
        return self.comments.insert_one(comentario).inserted_id

    def obtener_comentarios(self):
        return list(self.comments.find())

    def actualizar_comentario(self, comentario_id, nuevos_datos):
        return self.comments.update_one({"_id": ObjectId(comentario_id)}, {"$set": nuevos_datos})

    def eliminar_comentario(self, comentario_id):
        return self.comments.delete_one({"_id": ObjectId(comentario_id)})

    def buscar_comentarios(self, filtro):
        """Buscar comentarios por texto, autor, artículo, etc."""
        return list(self.comments.find(filtro))

    def contar_comentarios(self, filtro=None):
        """Contar comentarios (con o sin filtro)"""
        return self.comments.count_documents(filtro or {})

    ##
    def obtener_articulos_con_autor(self):
        """Muestra artículos con el nombre del autor"""
        resultados = []
        for art in self.articles.find():
            autor = self.users.find_one({"_id": art["author_id"]})
            art["author_name"] = autor["name"] if autor else "Desconocido"
            resultados.append(art)
        return resultados

    def obtener_comentarios_de_articulo(self, articulo_id):
        """Muestra los comentarios de un artículo específico"""
        return list(self.comments.find({"article_id": ObjectId(articulo_id)}))

    def close(self):
        self.client.close()
######################################################################
def ejemplo():
    blog = BlogCompleto()

    print("Creando usuario...")
    user_id = blog.crear_usuario("Ana Developer", "ana@correo.com")

    print("Creando tags y categorías...")
    tag_id = blog.crear_tag("python", "python-url")
    cat_id = blog.crear_categoria("programación", "prog-url")

    print("Creando artículo relacionado con usuario, tag y categoría...")
    art_id = blog.crear_articulo(
        "Mi primer artículo",
        "Contenido del artículo...",
        user_id,
        tags=[tag_id],
        categorias=[cat_id]
    )

    print("Agregando comentario...")
    comment_id = blog.crear_comentario(art_id, user_id, "Excelente artículo!")

    print("Artículos con autor:")
    for a in blog.obtener_articulos_con_autor():
        print(a)

    print("Comentarios del artículo:")
    for c in blog.obtener_comentarios_de_articulo(art_id):
        print(c)

    blog.close()


if __name__ == "__main__":
    ejemplo()