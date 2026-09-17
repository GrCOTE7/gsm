"""Zone défilante prête à l'emploi : scrollbar + gouttière anti-chevauchement.

Le problème résolu
------------------
Dans Flet 1.0, `ft.Scrollbar` n'expose **aucune marge** : ses seuls champs sont
`thumb_visibility`, `track_visibility`, `thickness`, `radius`, `interactive` et
`orientation`. Flutter peint la scrollbar *par-dessus* le contenu, dans la
boîte du viewport scrollable : tout contenu aligné à droite (valeurs, boutons,
badges) finit donc chevauché par le pouce.

Deux pièges vérifiés en conditions réelles :

1. Mettre le padding sur un `Container` **extérieur** ne corrige rien — la
   scrollbar se place sur le bord du *viewport scrollable*, pas sur celui du
   Container. Il faut réserver la marge **à l'intérieur** du contenu défilant.
2. `ft.Column` n'accepte pas de paramètre `padding` dans cette version
   (`Column.__init__() got an unexpected keyword argument 'padding'`), et
   `ft.Padding.only(...)` est la bonne fabrique — `ft.padding.only(...)` lève
   `module 'flet.controls.padding' has no attribute 'only'`.

L'invariant qui fait marcher le tout
------------------------------------

`GUTTER` est la largeur de la bande réservée, **et** l'épaisseur passée à la
scrollbar. La barre recouvre donc *exactement* cette bande : le contenu s'arrête
pile au bord gauche du pouce.

C'est ce qui distingue une correction d'un simple réglage cosmétique. Sans bande
réservée (l'état d'origine), la barre passe par-dessus les valeurs alignées à
droite. Avec une bande, plus rien n'est recouvert — même avec une valeur
suffisamment longue pour remplir toute la largeur disponible, cas où l'on voit
le contenu buter précisément contre le pouce sans passer dessous.

Utilisation
-----------
Le cas courant, sur n'importe quelle page ::

    from gsm.ui import ScrollArea

    return ScrollArea.column(
        controls=[
            ft.Text("Titre"),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[...]),
        ],
        height=400,
    )

`ScrollArea.column()` applique la gouttière à **chaque enfant**. Les enfants
produits par `gutter()` (ou par les helpers qui l'utilisent déjà) ne doivent
donc pas être passés ici : ce serait 2 x `GUTTER` de marge.
"""

import flet as ft

# Largeur de la bande réservée à droite du contenu défilant.
#
# INVARIANT : cette bande est dimensionnée pour être *entièrement* recouverte
# par la barre (voir `ScrollArea.scrollbar()`, qui reçoit `thickness=GUTTER`).
# Le contenu s'arrête donc exactement au bord gauche du pouce : ni chevauchement,
# ni jeu inutile.
#
# Corollaire : ne jamais régler l'épaisseur de la barre séparément de GUTTER.
# Une barre plus fine que la bande laisse un trou ; une barre plus large repasse
# par-dessus le contenu — exactement le bug d'origine.
GUTTER = 12  # px

# Conservé pour la lisibilité des appelants : la barre fait la largeur de la bande.
SCROLLBAR_THICKNESS = GUTTER  # px


def gutter(control: ft.Control) -> ft.Control:
    """Décale `control` pour le libérer d'une scrollbar verticale.

    À utiliser pour tout contenu susceptible d'atteindre le bord droit du
    viewport défilant (ligne de valeurs, séparateur, contrôle pleine largeur).
    Pour une zone entièrement défilante, préférer `ScrollArea.column()`, qui
    l'applique à tous ses enfants.

    Args:
        control: Le contrôle à décaler.

    Returns:
        `control` enveloppé dans un `Container` réservant `GUTTER` px à droite.
    """
    return ft.Container(
        padding=ft.Padding.only(right=GUTTER),
        content=control,
    )


class ScrollArea:
    """Fabrique de contrôles défilants dont le contenu ne passe pas sous la barre.

    Classe-namespace à méthodes statiques, comme `Header` ou `DiagnosticBlock` :
    aucune instance à créer. Les méthodes ne sont volontairement **pas**
    décorées `@ft.component` — elles n'utilisent aucun hook, donc elles
    retournent un control composable aussi bien depuis un composant que
    directement (`page.add(ScrollArea.column(...))`).
    """

    THICKNESS = SCROLLBAR_THICKNESS
    GUTTER = GUTTER

    @staticmethod
    def gutter(control: ft.Control) -> ft.Control:
        """Alias de `gutter()`, exposé pour un point d'entrée unique."""
        return gutter(control)

    @staticmethod
    def scrollbar(
        thickness: int = GUTTER,
    ) -> ft.Scrollbar:
        """Config de scrollbar dimensionnée pour remplir la gouttière.

        Args:
            thickness: Épaisseur en px. La valeur par défaut (`GUTTER`) fait
                coïncider la barre avec la bande réservée par `gutter()` — c'est
                ce qui garantit l'absence de chevauchement. Ne la diminuer que si
                vous diminuez aussi `GUTTER`.
        """
        return ft.Scrollbar(
            thickness=thickness,
            thumb_visibility=True,
        )

    @staticmethod
    def column(
        controls: list[ft.Control],
        *,
        height: int | None = None,
        expand: bool = False,
        spacing: int = 16,
        scroll: ft.Scrollbar | None = None,
    ) -> ft.Column:
        """`Column` défilante dont chaque enfant est décalé de la gouttière.

        Volontairement **sans paramètre `padding`** : la marge extérieure se pose
        chez l'appelant, via un `ft.Container(padding=...)` autour de cette
        colonne. Un tel paramètre ici serait écrasé dès que l'appelant en passe
        un, ce qui donne l'illusion d'un réglage inopérant.

        Args:
            controls: Enfants de la colonne. Ne pas y mettre de contrôles déjà
                passés par `gutter()`.
            height: Hauteur fixe en px. Laisser `None` avec `expand=True` pour
                occuper la place disponible.
            expand: Étire la colonne dans son parent.
            spacing: Espace vertical entre les enfants.
            scroll: Config de scrollbar ; par défaut `scrollbar()`.

        Returns:
            Une `ft.Column` défilante.
        """
        return ft.Column(
            spacing=spacing,
            height=height,
            expand=expand,
            scroll=scroll if scroll is not None else ScrollArea.scrollbar(),
            controls=[gutter(ctrl) for ctrl in controls],
        )
