def reset_statistic(modeladmin, request, queryset):
    for team in queryset:
        team.reset_statistic()
        team.save()


def calibrate_score(modeladmin, request, queryset):
    for team in queryset:
        team.calibrate_score()
        team.save()


reset_statistic.short_description = "Reset team statistic"
calibrate_score.short_description = "Calibrate team score"
