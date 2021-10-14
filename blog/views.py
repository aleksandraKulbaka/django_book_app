from django.shortcuts import render

posts = [
    {
        'author': 'AWK',
        'bookTitle': 'Hobbit',
        'bookAuthor': 'J.R.R. Tolkien',
        'review': 5,
        'date': 'August 20, 2021'
    },
    {
        'author': 'AWK',
        'bookTitle': 'Lord of the Rings: The Two Towers',
        'bookAuthor': 'J.R.R. Tolkien',
        'review': 5,
        'date': 'September 01, 2021'
    },
    {
        'author': 'AWK',
        'bookTitle': "Ranger's apprentice: The Ruins of Gorlan",
        'bookAuthor': 'John Flanagan',
        'review': 5,
        'date': 'October 11, 2021'
    }
]
def home(request):
    context = {
        'posts': posts,
    }
    return render(request, 'blog/home.html', context)

    # Create your views here.
def about(request):
    return render(request, 'blog/about.html')