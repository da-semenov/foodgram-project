from django import template

register = template.Library()

TAGS = {
        'breakfast': 'orange',
        'lunch': 'green',
        'dinner': 'purple'
    }


@register.filter
def url_with_get(request, page):
    query = request.GET.copy()
    query['page'] = page
    return query.urlencode()


@register.filter
def add_color(tag):
    colors = TAGS
    return colors[tag.slug]


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def subtract(number_1, number_2):
    return int(number_1) - int(number_2)


@register.filter
def get_tags(request):
    return request.getlist('tag')


@register.filter
def renew_tag_link(request, tag):
    request_copy = request.GET.copy()
    tags = request_copy.getlist('tag')
    if tag.slug in tags:
        tags.remove(tag.slug)
        request_copy.setlist('tag', tags)
    else:
        request_copy.appendlist('tag', tag.slug)
    return request_copy.urlencode()


@register.filter
def tags_template(tags):
    return tags.values_list('slug', flat=True)


@register.filter
def conjoin(number, args):
    args = [arg.strip() for arg in args.split(',')]
    last_digit = int(number) % 10
    if last_digit == 1:
        return f'{number} {args[0]}'
    elif 1 < last_digit < 5:
        return f'{number} {args[1]}'
    elif last_digit > 4 or last_digit == 0:
        return f'{number} {args[2]}'
