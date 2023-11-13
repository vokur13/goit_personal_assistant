from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Note, Tag
from .forms import NoteForm, TagForm

# Отображение списка заметок
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

# Отображение деталей заметок
class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

# Создание заметки
class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'notes/note_form.html'
    form_class = NoteForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('notes:note_list')

# Редактирование заметки
class NoteEditView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'notes/note_form.html'
    form_class = NoteForm

    def get_success_url(self):
        return reverse('notes:note_list')

# Удаление заметки
class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('notes:note_list')

# Отображение списка тегов
class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'notes/tag_list.html'
    context_object_name = 'tags'

# Создание тега
class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = 'notes/tag_form.html'
    form_class = TagForm

    def get_success_url(self):
        return reverse('notes:tag_list')

# Редактирование тега
class TagEditView(LoginRequiredMixin, UpdateView):
    model = Tag
    template_name = 'notes/tag_form.html'
    form_class = TagForm

    def get_success_url(self):
        return reverse('notes:tag_list')

# Удаление тега
class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'notes/tag_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('notes:tag_list')