from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .classes import MadLibString
from .models import MadLib, WordList
from .forms import MadLibWordForm, MadLibForm, WordListForm


# Create your views here.
def home(request):
    context = {
        'nbar': 'home',
    }
    return render(request, 'mad_libs/home.html', context)


def mad_libs(request):
    context = {
        'nbar': 'mad-libs',
    }
    return render(request, 'mad_libs/mad-libs.html', context)


def mad_lib_detail(request, mad_lib_id):
    mad_lib = MadLib.objects.get(pk=mad_lib_id)
    word_list = list(WordList.objects.filter(mad_lib_id=mad_lib_id))
    word_form_set = formset_factory(MadLibWordForm, extra=len(word_list))
    story_result = list()

    if request.method == 'POST':
        method_is_post = True
        formset = word_form_set(request.POST)
        if formset.is_valid():
            input_words = list()
            for form in formset:
                input_words.append(form.cleaned_data.get('word').strip())
            story_strings = (mad_lib.story.split("___"))
            word_iterator = iter(input_words)
            for s in story_strings:
                if s == "---":
                    mls = MadLibString(next(word_iterator, ""), True)
                else:
                    mls = MadLibString(s, False)
                story_result.append(mls)
        else:
            method_is_post = False
    else:
        method_is_post = False
        formset = word_form_set()
        for i in range(len(word_list)):
            formset[i].fields['word'].label = word_list[i].word

    context = {
        'nbar': mad_lib_id,
        'mad_lib': mad_lib,
        'formset': formset,
        'story_result': story_result,
        'method_is_post': method_is_post
    }
    return render(request, 'mad_libs/mad-lib-details.html', context)


@login_required
def create_mad_lib(request):
    form = MadLibForm(request.POST or None)
    context = {
        'form': form,
    }

    if form.is_valid():
        create_word_list_items(form, request)
        return redirect('mad_libs:mad_libs')
    return render(request, 'mad_libs/mad-lib-form.html', context)


@login_required
def delete_mad_lib(request, mad_lib_id):
    mad_lib = MadLib.objects.get(pk=mad_lib_id)
    context = {
        'nbar': mad_lib.id,
        'mad_lib': mad_lib,
    }
    if request.method == 'POST':
        title = mad_lib.mad_lib_name
        mad_lib.delete()
        messages.success(request, f'Mad Lib {title} was deleted.')
        return redirect('mad_libs:mad_libs')
    return render(request, 'mad_libs/mad-lib-delete.html', context)


@login_required
def update_mad_lib(request, mad_lib_id):
    mad_lib = MadLib.objects.get(pk=mad_lib_id)
    word_list_items = WordList.objects.filter(mad_lib_id=mad_lib.id).order_by('position')
    word_list = ""
    for i in range(len(word_list_items)):
        word_list += str(word_list_items[i].word)
        if i != len(word_list_items) - 1:
            word_list += ", "
    form = MadLibForm(request.POST or None, initial={'word_list': word_list}, instance=mad_lib)
    context = {
        'nbar': mad_lib.id,
        'mad_lib': mad_lib,
        'form': form,
    }
    if form.is_valid():
        WordList.objects.filter(mad_lib_id=mad_lib.id).delete()
        create_word_list_items(form, request)
        return redirect('mad_libs:mad_libs')
    return render(request, 'mad_libs/mad-lib-form.html', context)


def create_word_list_items(form, request):
    new_mad_lib = form.save()
    word_list_data = str(form.cleaned_data.get('word_list')).split(",")
    counter = 1
    for item in word_list_data:
        WordList.objects.create(mad_lib_id_id=new_mad_lib.id, word=str(item).strip().upper(), position=counter)
        counter += 1
    messages.success(request, f'Mad Lib {form.cleaned_data.get("mad_lib_name")} was created.')


@login_required
def create_word_list(request):
    form = WordListForm(request.POST or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        messages.success(request, f'Word List Item {form.cleaned_data.get("id")} was created.')
        return redirect('mad_libs:mad_libs')
    return render(request, 'mad_libs/word-list-form.html', context)
