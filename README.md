# drf-psq

[![Build Status](https://travis-ci.org/drf-psq/drf-psq.svg?branch=master)](https://travis-ci.org/drf-psq/drf-psq)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/115a206999004ff0b0196e7b48a856a6)](https://www.codacy.com/gh/drf-psq/drf-psq?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=drf-psq/drf-psq&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/drf-psq/drf-psq/branch/master/graph/badge.svg)](https://codecov.io/gh/drf-psq/drf-psq)
[![License: MIT](https://img.shields.io/github/license/drf-psq/drf-psq.svg)](https://github.com/drf-psq/drf-psq/blob/master/LICENSE)
[![PyPI version shields.io](https://img.shields.io/pypi/v/drf-psq.svg)](https://pypi.python.org/pypi/drf-psq)

`drf-psq` is an extension for the Django REST framework that gives support for having view-based **permission_classes**, **serializer_class**, and **queryset**.
In a typical DRF project, you probably have faced the problem that you want to set different permissions for different views with different serializers and you have to write too many `if` statements and override some methods to achieve this goal! Well, you don't have to do those kinds of hard stuff anymore. `drf-psq` is made to solve this problem and even more!

## Setup

### DRF Version

There is a bug in combining permission classes in DRF version `3.11.*` or lower. It is recommended to use DRF version `3.12.0` or higher. Check this [link](https://github.com/encode/django-rest-framework/pull/6605) out for more information.

### Install Package

```bash
pip install drf-psq
```

### Add to Project

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'drf_psq',
    ...
]
```

## Simple Usage

Consider this scenario:

* There is a `user` class.
* Admins can create new users or view a list of users with **complete** information on each user.
* Admins can view or edit users' **complete** information.
* Admins can delete a user.
* Each user can view or edit their **basic** information.

In a typical DRF project, you would probably implement the code below for this scenario:

```python
class IsSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserFullSerializer
    permission_classes = [IsAdminUser]


    def get_serializer_class(self):
        cond1 = bool(self.action in ['retrieve', 'update', 'partial_update'])

        obj = self.get_object()
        cond2 = bool(
            IsAuthenticated.has_permission(self.request, None) and
            IsSelf.has_object_permission(self.request, None, obj)
        )

        if cond1 and cond2:
            return UserBasicSerializer

        return super().get_serializer_class()


    def get_permission_classes(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [(IsAuthenticated & IsSelf) | IsAdminUser]

        return super().get_permission_classes()
```

This implementation has too many unrelated codes to views' logic and also in more complex scenarios, there would be a higher chance of making mistakes and causing bugs.
But, there is no need to implement these enormous amounts of hard codes in every viewset of each project. Using `drf-psq` all these codes can be replaced by only a configuration dictionary.

Now let `drf-psq` do the work:

```python
from drf_psq import PsqMixin, Rule, psq

class UserViewSet(PsqMixin, viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserFullSerializer
    permission_classes = [IsAdminUser]

    psq_rules = {
        ('retrieve', 'update', 'partial_update'): [
            Rule([IsAdminUser], UserFullSerializer),
            Rule([IsAuthenticated & IsSelf], UserBasicSerializer)
        ]
    }
```

Well, it seems much more simple!

Now let's take a look at each component of this extension and put them all together in a complete example.

## Components

### 1. PsqMixin class

A mixin that contains logics of `drf-psq` and viewsets must inherit it in order to enable `psq` functionalities. Make sure that this mixin is the first one on the list of inherited classes. All the access rules should be defined in the `psq_rules` dictionary.

### 2. psq_rules dictionary

A dictionary that contains access rules. Keys can be strings or tuples of strings, indicating the name of the view(s). Values are a list of `Rule` classes. Each `Rule` class contains information about an access rule. More details are provided in the later subsections.

* **Important note:** The roles in the mentioned list will be checked respectively and their order matters. The first matched rule will be selected to be applied. If none of them matches, the action will not be performed.

### 3. psq decorator

A decorator that can be used instead of `psq_rules` dictionary in case you are a fan of decorators in python! Also, it is possible to combine both `psq decorators` and `psq_rules` and use them at the same time.

Example:

```python
class UserViewSet(PsqMixin, viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserBasicSerializer
    permission_classes = [IsAuthenticated]

    @psq([
        Rule([IsAdminUser], UserFullSerializer),
        Rule([IsAuthenticated], UserBasicSerializer)
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

### 4. Rule class

A class that holds any information required for an access rule. Its attributes are explained below. It is to be noted that the default values declared in the viewset class (or settings) will be considered as the default value for all these attributes.

#### 4.1. permission_classes

A list of permission classes that specifies who has access to this rule.

#### 4.2. serializer_class

A serializer class which will be used for serializing objects related to this access rule.

#### 4.3. queryset

A *lambda* function that enables you to use different querysets for each access rule. This *lambda* function takes `self` (the viewset class) as its argument.

Here is an example that allows admin users to get a list of all users with their complete information, while other authenticated users can only get a list of non-admin users with their basic information:

```python
class UserViewSet(PsqMixin, viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserFullSerializer
    permission_classes = [IsAdminUser]

    psq_rules = {
        'list': [
            Rule([IsAdminUser]),
            Rule(
                [IsAuthenticated],
                UserBasicSerializer,
                lambda self: User.objects.filter(is_superuser=False, is_staff=False)
            )
        ]
    }
```

#### 4.4. get_obj

*In my opinion, this is the coolest feature in this extension!*

A *lambda* function that enables you to support object-level permissions in associated models to the main model. It takes `self` (the viewset class), and `obj` (the object returns by **get_object** method) as its arguments.

For example, consider this scenario: we have some libraries that each one contains some books. Each user can register in just one library (for simplicity's sake). Now you want to implement a mechanism to allow users to only access the books in the library they have registered at. Let's see how its code will be by using `drf-psq`.

```python
################################### Models ###################################

from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=50)

class Book(models.Model):
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True)

class User(models.Model):
    registered_library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True)


################################ Permissions #################################

from rest_framework import permissions


class IsRegisteredInLibrary(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):  # 'obj' is of type Library
        return request.user.registered_library == obj


################################### Views ####################################

from rest_framework import viewsets
from rest_framework import mixins

from drf_psq import PsqMixin, Rule, psq


class LibraryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsRegisteredInLibrary]


class BookViewSet(PsqMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsRegisteredInLibrary]

    psq_rules = {
        'retrieve': [Rule(get_obj=lambda self, obj: obj.library)]
    }
```

So, you can avoid creating too many redundant permission classes for each associated model.

## A Complete Example

The complete source code of our library example can be found [here](https://github.com/drf-psq/drf-psq/tree/master/examples/library).

## Acknowledgments

* Thanks to [@jooof](https://github.com/jooof) for his brilliant opinions and suggestions.
