def reset_statistic(modeladmin, request, queryset):
    for team in queryset:
        team.reset_statistic()
        team.save()


reset_statistic.short_description = "Reset team statistic"
