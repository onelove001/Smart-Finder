from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from core.models import customUser
from chat.timesin import calcEpochSec, timesince
import datetime

