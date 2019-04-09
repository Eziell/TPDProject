Sys.setenv(JAVA_HOME='C:\\Program Files\\Java\\jre1.8.0_201')

install.packages("openxlsx")
library(openxlsx)

###------------------------------------------------------------###
###                        User Table                          ###
###------------------------------------------------------------###

# create data frame
users <- read.xlsx("user_table_sqlazure.xlsx", 
                   na.strings = c("NULL", "Não identificado"))

# variables correction
users$id_user <- factor(users$id_user)
users$id_user_original <- factor(users$id_user_original)
users$birthdate <- as.Date(users$birthdate)
users$gender <- factor(users$gender)
users$club <- factor(users$club)
users$region <- factor(users$region)
users$date_start_original <- as.Date(users$date_start_original)
users$zipcode_locality <- factor(users$zipcode_locality)
users$zipcode_desig <- factor(users$zipcode_desig)
users$name_locality <- factor(users$name_locality)
users$name_county <- factor(users$name_county)
users$name_district <- factor(users$name_district)
users$name_country <- factor(users$name_country)
users$date_start_season <- as.Date(users$date_start_season)
users$premium_date <- as.Date(users$premium_date)
users$agegroup <- factor(users$agegroup)
users$in_league <- as.logical(users$in_league)
users$row_effective_date <- as.Date(users$row_effective_date)
users$row_expiration_date <- as.Date(users$row_expiration_date)
users$row_timestamp <- as.Date(users$row_timestamp)
users$is_current_row <- as.logical(users$is_current_row)

str(users)

# summary
summary_users <- as.data.frame(summary(users))
write.xlsx(summary_users, "summary_userTable.xlsx")


###------------------------------------------------------------###
###                        Season Table                        ###
###------------------------------------------------------------###

# create data frame
season <- read.xlsx("season_table_sqlazure.xlsx")

# variables correction
season$id_season <- factor(season$id_season)
season$date_start <- as.Date(season$date_start)
season$date_end <- as.Date(season$date_end)
season$is_updated_game_version <- factor(season$is_updated_game_version)
season$is_variable_weekday_publish_date <- factor(season$is_variable_weekday_publish_date)
season$team_player_transfers_allowed_per_month <- factor(season$team_player_transfers_allowed_per_month)

str(season)

# summary
summary_season <- as.data.frame(summary(season))
write.xlsx(summary_season, "summary_seasonTable.xlsx")

###------------------------------------------------------------###
###                        Team Table                          ###
###------------------------------------------------------------###

# create data frame
teams <- read.xlsx("team_table_sqlazure.xlsx")

# variables correction
teams$id_team <- factor(teams$id_team)
teams$id_team_original <- factor(teams$id_team_original)
teams$createdate <- as.Date(teams$createdate)
teams$origin <- factor(teams$origin)
teams$is_paid <- factor(teams$is_paid)
teams$in_league <- factor(teams$in_league)

str(teams)

# summary
summary_teams <- as.data.frame(summary(teams))
write.xlsx(summary_teams, "summary_teamsTable.xlsx")

###------------------------------------------------------------###
###                        Date Table                          ###
###------------------------------------------------------------###

# create data frame
date <- read.xlsx("date_table_sqlazure.xlsx")

# variables correction
date$id_date <- factor(date$id_date)
date$day <- as.Date(date$day)
date$day_month <- factor(date$day_month)
date$calendar_month <- factor(date$calendar_month)
date$month <- factor(date$month)
date$Full <- as.Date(date$Full)
date$weekday <- factor(date$weekday)
date$calendar_weekday <- factor(date$calendar_weekday)
date$weekend_indicator <- as.logical(date$weekend_indicator)
date$round_order <- factor(date$round_order)
date$is_round_publication_day <- factor(date$is_round_publication_day)
date$is_round_end_day <- factor(date$is_round_end_day)
date$is_round_start_day <- factor(date$is_round_start_day)
date$is_before_game_starts <- factor(date$is_before_game_starts)
date$is_after_game_ends <- factor(date$is_after_game_ends)
date$is_winter_transfer_season <- factor(date$is_winter_transfer_season)
date$Year <- factor(date$Year)

str(date)

# summary
summary_date <- as.data.frame(summary(date))
write.xlsx(summary_date, "summary_dateTable.xlsx")
