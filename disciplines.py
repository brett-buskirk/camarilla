import discord


def discipline_details(discipline, db):
    # Retrieve the disciplines collection
    collection = db['disciplines']

    # Make sure discipline exists in collection
    try:
        details = collection.find_one({"name": discipline.lower()})
        discipline_name = details["name"]
    except Exception:
        embed = discord.Embed(
            title=f'Sorry, cannot find the {discipline} discipline',
            color=discord.Colour.dark_red()
        )
        return embed

    # Create the embed to send to server
    embed = discord.Embed(
        title=f'{discipline_name.upper()}',
        color=discord.Colour.dark_red()
    )
    embed.set_thumbnail(url='https://i.imgur.com/MYTRmLX.png')
    for level in ['level1', 'level2', 'level3', 'level4', 'level5']:
        for power in details[level]:
            embed.add_field(name=f'[{level[-1]}] {power["name"].upper()}', value=power["description"], inline=False)

    embed.set_footer(text='Core Rulebook, page 244')

    print(details)
    return embed


def discipline_power(discipline, power, db):
    # Retrieve the discipline collection
    collection = db['disciplines']

    # Retrieve the discipline document
    discipline_data = collection.find_one({"name": discipline})

    # Get the specific power
    power_data = False
    power_level = 0
    for level in ['level1', 'level2', 'level3', 'level4', 'level5']:
        for pwr in discipline_data[level]:
            if pwr['name'] == power:
                power_data = pwr
                power_level = level[-1]

    if not power_data:
        embed = discord.Embed(
            title=f'Sorry, cannot find the power: {power}',
            color=discord.Colour.dark_red()
        )
        return embed

    # Create embed to send to server
    embed = discord.Embed(
        title=f'{power_data["name"].upper()} ({discipline.title()} {power_level})',
        color=discord.Colour.dark_red()
    )
    embed.add_field(name="Amalgam", value=power_data["amalgam"], inline=False)
    embed.add_field(name="Description", value=power_data["description"], inline=False)
    embed.add_field(name="Dice", value=power_data["dice"], inline=False)
    embed.add_field(name="Cost", value=power_data["cost"], inline=False)
    embed.add_field(name="System", value=power_data["system"], inline=False)
    embed.set_footer(text=power_data["page"])

    return embed


def discipline_list(db):
    # Retrieve the discipline collection
    collection_name = db["disciplines"]

    # Get all the discipline documents
    disciplines = collection_name.find()

    # Create the embed
    embed = discord.Embed(
        title='Vampire Disciplines',
        color=discord.Colour.dark_red()
    )
    for discipline_name in disciplines:
        embed.add_field(
            name=discipline_name['name'].title(),
            value="\u200b",
            inline=False
        )
    embed.set_footer(text='Core Rulebook, page 243')

    return embed
