# Bullshit spawn rates

import asyncio
from random import randint, random

from discord.ext import commands
from discord.ext.commands import BucketType

from nyxbot.nyxutils import reply

ranks = ["N", "R", "SR", "SSR"]
probs = [0.00, 0.70, 0.24, 0.06]
pools = [[], [], [], []]
emoji = [":blue_circle:", "<:rare:270755777457684480>",
         "<:srare:270755873624817664>", "<:ssrare:270755922874335232>"]

things = []
url_prefix = "http://unisonleague.fandom.com/wiki/"


class SpawnItem:
    def __init__(self, name, url, rarity):
        self.name = name
        self.url = url
        self.rank = rarity
        global pools
        # for i in range(0, int(prob * 100)):
        pools[rarity].append(self)


def load():
    # R, formerly with prob rating of 1.0
    SpawnItem("Swelter Taurus", "Swelter_Taurus_(Gear)", 1)
    SpawnItem("Swelter Kong", "Swelter_Kong_(Gear)", 1)
    SpawnItem("Kin-ki", "Kin-ki_(Gear)", 1)
    SpawnItem("Croc Man", "Croc_Man_(Gear)", 1)
    SpawnItem("Mermaid", "Mermaid_(Gear)", 1)
    SpawnItem("Sea Serpent", "Sea_Serpent_(Gear)", 1)
    SpawnItem("Inky", "Inky_(Gear)", 1)
    SpawnItem("Kotaro the Stray Cat", "Kotaro_the_Stray_Cat_(Gear)", 1)
    SpawnItem("Crow Tengu", "Crow_Tengu_(Gear)", 1)
    SpawnItem("Kaava", "Kaava_(Gear)", 1)
    SpawnItem("Unicorn", "Unicorn_(Gear)", 1)
    SpawnItem("Exia Knight", "Exia_Knight_(Gear)", 1)
    SpawnItem("Val Leo", "Val_Leo_(Gear)", 1)
    SpawnItem("Banshee", "Banshee_(Gear)", 1)
    SpawnItem("Wyvern", "Wyvern_(Gear)", 1)
    SpawnItem("Medusa", "Medusa_(Gear)", 1)
    SpawnItem("Dullahan", "Dullahan_(Gear)", 1)
    SpawnItem("Cyclops", "Cyclops_(Gear)", 1)
    SpawnItem("Petrasaur", "Petrasaur_(Gear)", 1)
    SpawnItem("Golem", "Golem_(Gear)", 1)
    # SR
    SpawnItem("Firedrake Ignis", "Firedrake_Ignis_(Gear)", 2)
    SpawnItem("Ninetail Fox", "Ninetail_Fox_(Gear)", 2)
    SpawnItem("Leviathan", "Leviathan_(Gear)", 2)
    SpawnItem("Fenrir", "Fenrir_(Gear)", 2)
    SpawnItem("Hraesvelgr", "Hraesvelgr_(Gear)", 2)
    SpawnItem("Cuchulainn", "Cuchulainn_(Gear)", 2)
    SpawnItem("Etherful Golem", "Etherful_Golem_(Gear)", 2)
    SpawnItem("Physoth, Sacred Beast", "Physoth,_Sacred_Beast_(Gear)", 2)
    SpawnItem("Diablos", "Diablos_(Gear)", 2)
    SpawnItem("Metus, Evil Drake", "Metus,_Evil_Drake_(Gear)", 2)
    # SSR: http://unisonleague.wikia.com/wiki/Monster_Encyclopedia/SSR

    # Fire SSRs
    # SpawnItem("", "_(Gear)", 3)
    SpawnItem("Behemoth", "Behemoth_(Gear)", 3)
    SpawnItem("Kagutsuchi", "Kagutsuchi_(Gear)", 3)
    SpawnItem("Joan of Arc", "Joan_of_Arc_(Gear)", 3)
    SpawnItem("Nobunaga", "Nobunaga_(Gear)", 3)
    SpawnItem("Salamander", "Salamander_(Gear)", 3)
    SpawnItem("Surtr", "Surtr_(Gear)", 3)
    SpawnItem("Espada", "Espada_(Gear)", 3)

    # Water SSRs
    # SpawnItem("", "_(Gear)", 3)
    SpawnItem("Poseidon", "Poseidon_(Gear)", 3)
    SpawnItem("Siren", "Siren_(Gear)", 3)
    SpawnItem("Andromeda", "Andromeda_(Gear)", 3)
    SpawnItem("Ushiwakamaru", "Ushiwakamaru_(Gear)", 3)
    SpawnItem("Tsuyukusa", "Tsuyukusa_(Gear)", 3)
    SpawnItem("Tyr", "Tyr_(Gear)", 3)

    # Wind SSRs
    # SpawnItem("", "_(Gear)", 3)
    SpawnItem("Quetzalcoatl", "Quetzalcoatl_(Gear)", 3)
    SpawnItem("Shinatobe, Wind Caller", "Shinatobe,_Wind_Caller_(Gear)",
              3)
    SpawnItem("Kirin", "Kirin,_the_Wind_Beast_(Gear)", 3)
    SpawnItem("Artemis", "Artemis_(Gear)", 3)
    SpawnItem("Sun Wukong", "Sun_Wukong_(Gear)", 3)
    SpawnItem("Gigantes", "Gigantes_(Gear)", 3)
    SpawnItem("Freya", "Freya_(Gear)", 3)

    # Light SSRs
    # SpawnItem("", "_(Gear)", 3)
    SpawnItem("Valkyrie", "Valkyrie_(Gear)", 3)
    SpawnItem("Indra, Storm God", "Indra,_Storm_God_(Gear)", 3)
    SpawnItem("Nezha", "Nezha_(Gear)", 3)
    SpawnItem("Venus", "Venus_(Gear)", 3)
    SpawnItem("Aladdin", "Aladdin_(Gear)", 3)
    SpawnItem("Nesha", "Nesha_(Gear)", 3)

    # Dark SSRs
    # SpawnItem("", "_(Gear)", 3)
    SpawnItem("Lilith", "Lilith_(Gear)", 3)
    SpawnItem("Aizen", "Aizen_(Gear)", 3)
    SpawnItem("Anubis the Protector", "Anubis_the_Protector_(Gear)", 3)
    SpawnItem("Hel", "Hel_(Gear)", 3)
    SpawnItem("Yashamaru", "Yashamaru_(Gear)", 3)
    SpawnItem("Christiana", "Christiana_(Gear)", 3)

    # Haste SSRs
    # SpawnItem("", "_(Gear)", 3)
    SpawnItem("Hades", "Hades_(Gear)", 3)
    return True


class UnisonSpawn(commands.Cog):
    def __init__(self, nyx):
        self.nyx = nyx

    @commands.command(aliases=["spawnmonster"])
    @commands.cooldown(1, 2, BucketType.user)
    async def spawn(self, ctx, amount: int = 1):
        """Brings forth a rush of salt...
        The amount spawned has to be between 1 and 10 inclusive.

        Dedicated to our old friend RusyChicken, who had the original RNGesus
        spawning bot.
        """
        if amount < 1 or amount > 10:
            await reply(ctx, "WTF?!")
            ctx.command.reset_cooldown(ctx)
            return
        msg = await ctx.channel.send("Spawning...\n:blue_circle: >>>>")
        spawn_ten = amount == 10
        spawned = []
        top_rank = 0
        for i in range(0, amount):
            pick = random()
            prob = 0
            rare = 0
            for i in range(0, len(pools)):
                prob += probs[i]
                if pick > prob:
                    rare += 1
            pool = pools[rare]
            spawn = pool[randint(0, len(pool) - 1)]
            spawned.append(spawn)
            top_rank = max(top_rank, spawn.rank)
        await asyncio.sleep(1)
        if top_rank == 1 and not spawn_ten:
            await msg.edit(
                content="Spawning...\n:blue_circle: >>>>>>>> " + emoji[
                    1])
        else:
            await msg.edit(content=" ".join(
                ["Spawning...\n:blue_circle: >>>>>>>>", emoji[1],
                 ">>>>"]))
            if spawn_ten and top_rank == 1:
                spawned[randint(0, len(spawned) - 1)] = pools[2][
                    randint(0, len(pools[2]) - 1)]
                top_rank = 2
            await asyncio.sleep(1)
            if top_rank == 2:
                await msg.edit(content=" ".join(
                    ["Spawning...\n:blue_circle: >>>>>>>>", emoji[1],
                     ">>>>>>>>", emoji[2]]))
            else:
                await msg.edit(content=" ".join(
                    ["Spawning...\n:blue_circle: >>>>>>>>", emoji[1],
                     ">>>>>>>>", emoji[2], ">>>>"]))
                await asyncio.sleep(1)
                await msg.edit(content=" ".join(
                    ["Spawning...\n:blue_circle: >>>>>>>>", emoji[1],
                     ">>>>>>>>", emoji[2], ">>>>>>>>", emoji[3]]))
        await asyncio.sleep(1)
        if amount > 1:
            decor = ["Spawning:\n"]
            for spawn in spawned:
                decor.append(emoji[spawn.rank] + " ")
            await msg.edit(content="".join(decor).strip())
            await asyncio.sleep(2)
        await msg.delete()
        if amount > 1:
            msg = ["Congratulations! You spawned the following:"]
            top_url = None
            for spawn in spawned:
                msg.append("".join(["\n", spawn.name, " (", ranks[spawn.rank],
                                    ") at " + ("%.2f" % (
                                            probs[spawn.rank] * 100 / len(
                                        pools[spawn.rank]))),
                                    "% probability."]))
                if spawn.rank == 3:
                    msg.extend(["\n", url_prefix, spawn.url])
                elif top_rank == spawn.rank and top_url is None:
                    top_url = "".join(["\n", url_prefix, spawn.url])
            if top_url is not None:
                msg.append(top_url)
            msg = "".join(msg)
        else:
            spawned = spawned[0]
            msg = "".join(["Congratulations! You spawned ", spawned.name, " (",
                           ranks[spawned.rank], ") at ", ("%.2f" % (
                        probs[spawned.rank] * 100 / len(
                    pools[spawned.rank]))), "% probability.\n", url_prefix,
                           spawned.url])
        await reply(ctx, msg)


def setup(nyx):
    load()
    nyx.add_cog(UnisonSpawn(nyx))
