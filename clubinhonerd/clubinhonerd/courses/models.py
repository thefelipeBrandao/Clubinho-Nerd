from django.db import models
from django.conf import settings


# para fazer consultadas no BD
# Manager customizado
class CourseManager(models.Manager):

	def search(self, query):
		# lista de models do BD com 'AND'
		# return self.get_queryset().filter(name__icontains=query, description__icontains=query)
		# lista de models do BD com 'OR'
		return self.get_queryset().filter(models.Q(name__icontains=query) | models.Q(description__icontains=query)) 
		

# chave primaria = primary_key = True
# Uma representação da tabela do BD
class Course(models.Model):

	name = models.CharField('Nome', max_length=100)
	slug = models.SlugField('Atalho')
	description = models.TextField('Descrição', blank=True)
	about = models.TextField('Sobre o Curso', blank=True)
	start_date = models.DateField('Data de Início', null=True, blank=True)
	# concatenado com o diretorio criado no settings / path
	image = models.ImageField(upload_to='courses/images', verbose_name='Imagem', null=True, blank=True) 
	create_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	objects = CourseManager() # um método que eu criei / adicionando ele no objects

	# retornar o nome do curso
	def __str__(self):
		return self.name

	# é bom criar ele quando um model tiver uma página só pra ele / para a url no barra de pesquisa
	@models.permalink	
	def get_absolute_url(self):
		#              url      url nomeada
		return ('details', (), { 'slug': self.slug })	

	#  nomes dos campos lá na página do admin
	class Meta:
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['name']	



# Inscrição de um user em um curso
class Enrollment(models.Model):

	STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	)

	user = models.ForeignKey(settings.AUTH_USER_MODEL,
		verbose_name='Usuário', related_name='enrollments', on_delete=models.PROTECT
	)
	course = models.ForeignKey(Course, 
		verbose_name='Course',related_name='enrollments', on_delete=models.PROTECT
	)
	# Status da inscrição
	status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)
	create_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	# ativar status do aluno
	def active(self):
		self.status = 1
		self.save()

	# Verificando se a inscrição foi aprovada
	def is_approved(self):
		return self.status == 1


	class Meta:
		verbose_name = 'Inscrição'
		verbose_name_plural = 'Inscrições'
		# para evitar repetições no BD
		unique_together = (('user', 'course'),)


class Announcement(models.Model):
	
	course = models.ForeignKey(Course,
		verbose_name='Curso', on_delete=models.PROTECT
	)
	title = models.CharField('Título', max_length=100)
	content = models.TextField('Conteúdo')
	create_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	def __str__(self):
		return self.title

	class Meta():
		verbose_name = 'Anúncio'
		verbose_name_plural = 'Anúncios'
		# ordenado de forma decrescente
		ordering = ['-create_at']


class Comment(models.Model):
	
	announcement = models.ForeignKey(Announcement, 
		verbose_name='Anúncio',related_name='comments', on_delete=models.PROTECT
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
		verbose_name='Usuário', on_delete=models.PROTECT
	)
	comment = models.TextField('Comentário')
	create_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	class Meta():
		verbose_name = 'Comentário'
		verbose_name_plural = 'Comentários'
		# ordenado de forma crescente
		ordering = ['create_at']
		





# ________________BD_____________________

# object é um Manager
# Course.object.all() = retorna tudo / ".all" = é um atalho
# Course.object.filter(name='', age=''...) = filtrando com AND
# Course.object.filter(name__icontains='Python') = ver se o nome contem tal nome
# Course.object.filter(name__iexact='MAIUSCULO') = ver se o nome contem tal nome
# Course.delete() = deleta todos
# Course.create(...) - inserir