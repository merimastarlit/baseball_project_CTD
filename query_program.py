
import sqlite3


def main():
    conn = sqlite3.connect("baseball.db")
    cursor = conn.cursor()

    while True:
        print("\n=== Baseball Stats Query Menu ===")
        print("1. Filter by Year")
        print("2. Filter by Stat (HR, RBI, SB)")
        print("3. Show only winning teams (> .500)")
        print("4. Combine Filters")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "5":
            print("Exiting program.")
            break

        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid option. Please choose 1-5.")
            continue

        # Base query
        query = """
        SELECT 
            player_stats.year,
            player_stats.player,
            player_stats.stat_type,
            player_stats.value,
            player_stats.team,
            standings.win_pct
        FROM player_stats
        LEFT JOIN standings
            ON player_stats.year = standings.year
            AND player_stats.team = standings.team
        WHERE 1=1
        """

        params = []

        # Option 1: Year
        if choice == "1" or choice == "4":
            year = input("Enter year (2015-2025): ")
            if year:
                query += " AND player_stats.year = ?"
                params.append(year)

        # Option 2: Stat
        if choice == "2" or choice == "4":
            stat = input("Enter stat (HR, RBI, SB): ").upper()
            if stat:
                query += " AND player_stats.stat_type = ?"
                params.append(stat)

        # Option 3: Winning teams
        if choice == "3" or choice == "4":
            winning = input("Winning teams only? (y/n): ").lower()
            if winning == "y":
                query += " AND standings.win_pct > 0.500"

        try:
            cursor.execute(query, params)
            results = cursor.fetchall()

            print(f"\nFound {len(results)} results.\n")
            for row in results[:10]:
                year, player, stat, value, team, win_pct = row

                print(f"Year: {year}")
                print(f"Player: {player}")
                print(f"Stat: {stat}")
                print(f"Value: {value}")
                print(f"Team: {team}")
                print(f"Win %: {win_pct}")
                print("-" * 30)

        except Exception as e:
            print("Error executing query:", e)

    conn.close()


if __name__ == "__main__":
    main()


# import sqlite3

# # Connect to the database
# conn = sqlite3.connect("./baseball.db")
# cursor = conn.cursor()


# query = """
# SELECT
#     player_stats.year,
#     player_stats.player,
#     player_stats.stat_type,
#     player_stats.value,
#     player_stats.team,
#     standings.win_pct
# FROM player_stats
# LEFT JOIN standings
#     ON player_stats.year = standings.year
#     AND player_stats.team = standings.team
# WHERE player_stats.year = ?
# AND player_stats.stat_type = ?
# AND standings.win_pct > 0.500
# """

# cursor.execute(query, (2022, "HR"))
# results = cursor.fetchall()
# print(len(results))
# print(results[:5])
# conn.close()
