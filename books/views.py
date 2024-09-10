from django.shortcuts import render
from books.models import Author, Book
from django.db.models import Sum, Count, Avg, Min, Max, OuterRef, Subquery


# 1) author's => book count 2) author's => max price book 3) author's => min price book 4) author's => min price average Aggregate va annotate orqali bajaringlar
# Create your views here.


def sample(request):
    # << 1ST TASK  author_total_books=Author.objects.annotate(book_count=Count('books')) >>
    
    # author_max_price=Author.objects.annotate(max_price=Max('books__price'))
    
    #<< 2ND TASK most_expensive_books=Book.objects.filter(author=OuterRef('pk')).order_by('-price')
    # authors_with_most_expensive_books=Author.objects.annotate(most_expensive_book=Subquery(most_expensive_books.values('title')[:1]),
    # most_expensive_price=Subquery(most_expensive_books.values('price')[:1])) >>

    # << 3RD TASK cheapest_books=Book.objects.filter(author=OuterRef('pk')).order_by('price')
    # authors_with_cheapest_books=Author.objects.annotate(cheapest_book=Subquery(cheapest_books.values('title')[:1]),
    # cheapest_price=Subquery(cheapest_books.values('price')[:1])) >>
    

    # 4RD TASK
    min_price_subquery=Book.objects.filter(author=OuterRef('pk')).values('price').order_by('price')[:1]
    authors_with_min_price=Author.objects.annotate(min_price=Subquery(min_price_subquery))
    average_min_price=authors_with_min_price.aggregate(min_price_avg=Avg('min_price'))
    context={
        # 'author_total_books':author_total_books,
        # 'authors_with_most_expensive_books': authors_with_most_expensive_books,
        # 'authors_with_cheap_books':authors_with_cheap_books,
        'authors_with_min_price': authors_with_min_price,
        'average_min_price': average_min_price['min_price_avg'],  
    }
    return render(request, 'books/index.html', context)