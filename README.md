# Stockfish — a powerful open-source chess engine

_.&nbsp;.&nbsp;.&nbsp;packaged for Fedora, CentOS, and OpenSUSE_

**What's a chess engine?**  
You know when you play a game of chess and choose "Play the computer?" The chess engine is _the computer_.

**Stockfish . . .**  
Stockfish is a free chess engine. It is not a complete chess program, but
requires a
[UCI-compatible](https://en.wikipedia.org/wiki/Universal_Chess_Interface)
graphical user interface (GUI) in order to be used comfortably (e.g.
[PyChess](https://github.com/taw00/pychess-rpm) (which I also build for
Fedora), [Gnome Chess](https://wiki.gnome.org/Apps/Chess), and many more). Read
the documentation for your GUI of choice for information about how to use
Stockfish with it. I recommend PyChess.

Stockfish, in recent years, has topped the list of strongest chess engines ever
developed. But it can be used by weak players as well, like myself, to learn
and analyze or just to have fun playing a game. PyChess, which I keep
recommending, allows you to tone down Stockfish's default capability to
bludgeon you to death with chess logic. :)

_**What is this GitHub Repository?**_

The purpose of this repository is to store all the bits and pieces needed to
build and package this application for various RPM flavors of Linux. The binary
(installable and runnable) packages are then built via the [Fedora Project's
COPR build system](https://copr.fedorainfracloud.org/coprs/taw/stockfish/).

I store all *my* contributions here needed to enable building and packaging
Stockfish.  Upstream code—for example, `Stockfish-sf_14.tar.gz`—will not be
redundantly stored here. Those can be found ...
[upstream](https://github.com/official-stockfish/Stockfish). If you know your
way around building RPMs, you will know how to work with the specfile and other
contributions found here.

# tl;dr&nbsp;.&nbsp;.&nbsp;.

## I just want to install Stockfish and play chess!

### [Fedora and CentOS]

**Prep&nbsp;.&nbsp;.&nbsp;.**
```bash
sudo dnf install -y dnf-plugins-core distribution-gpg-keys
sudo dnf copr enable taw/stockfish
```

**Install&nbsp;.&nbsp;.&nbsp;.**
```bash
# pychess is simply a linux chess frontend that I personally recommend
sudo dnf install -y stockfish pychess --refresh
```

### [OpenSUSE]

**Prep (Leap 15.X)&nbsp;.&nbsp;.&nbsp;.**
```sh
# Install GPG keys
sudo rpm --import https://download.copr.fedorainfracloud.org/results/taw/stockfish/pubkey.gpg
# Configure and enable the Stockfish repository
sudo echo "\
[copr:copr.fedorainfracloud.org:taw:stockfish]
name=Copr repo for stockfish owned by taw
baseurl=https://download.copr.fedorainfracloud.org/results/taw/stockfish/opensuse-tumbleweed-$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://download.copr.fedorainfracloud.org/results/taw/stockfish/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1
" > /etc/zypp/repos.d/_copr\:copr.fedorainfracloud.org\:taw\:stockfish.repo
sudo zypper refresh
```

**Prep (Tumbleweed)&nbsp;.&nbsp;.&nbsp;.**
```sh
# Install GPG keys
sudo rpm --import https://download.copr.fedorainfracloud.org/results/taw/stockfish/pubkey.gpg
# Configure and enable the Stockfish repository
sudo echo "\
[copr:copr.fedorainfracloud.org:taw:stockfish]
name=Copr repo for stockfish owned by taw
baseurl=https://download.copr.fedorainfracloud.org/results/taw/stockfish/opensuse-leap-$releasever-$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://download.copr.fedorainfracloud.org/results/taw/stockfish/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1
" > /etc/zypp/repos.d/_copr\:copr.fedorainfracloud.org\:taw\:stockfish.repo
sudo zypper refresh
```

**Install&nbsp;.&nbsp;.&nbsp;.**
```bash
# pychess is simply a linux chess frontend that I personally recommend
sudo zypper install stockfish pychess
```

## I installed it, now I want to play a game!

1. Open PyChess via your application menus.
2. Select a color for yourself and select Stockfish as your opponent
3. Play chess!

## More about&nbsp;.&nbsp;.&nbsp;.

* [Stockfish](https://stockfishchess.org/) — the Stockfish home website:<https://stockfishchess.org/>  
  `sudo dnf copr enable taw/stockfish`  
  `sudo dnf install stockfish --refresh -y`
* [PyChess](https://pychess.github.io/) — an excellent open-source feature-full
  chess frontend that can use Stockfish — recommend.  
  `sudo dnf install pychess --refresh -y`  
  Or install my build of Pychess (Fedora only!):  
  `sudo dnf copr enable taw/pychess`  
  `sudo dnf install pychess --refresh -y`
* [Gnome Chess](https://wiki.gnome.org/Apps/Chess) — another great open-source
  chess frontend that can use Stockfish. It has a particularly clean interface,
  but is a bit less versatile as compared to PyChess.  
  `sudo dnf install gnome-chess --refresh -y`
* [GNU Chess](https://www.gnu.org/software/chess/) — another chess engine that
  often is installed on Linux systems. It's not anywhere close to being as
  strong as Stockfish, but it's still stronger than you are at chess.  
  `sudo dnf install gnuchess --refresh -y`
* [LiChess.org](https://lichess.org/) — open-source and modern online chess.
  This is, IMHO, the best chess server out there. It's web interface is
  spectacular. It does not plug into the various desktop clients though (to avoid
  cheaters using chess hinting, etc). Some mobile applications plug in though.
* [Free Internet Chess Server (FICS)](https://www.freechess.org/) — One of the
  oldest and most popular chess servers. The web interface is awful and all
  play is done through an external client. Its default client is a Java Applet
  though, but since Java Applets are a thing of the past, setting up and
  managing your account is challenging to say the least. Once your account is set
  up, though, some clients, like PyChess, plug right in.
* Other open-source chess engines that work on Linux and seem to still be
  getting some development love: [Lc0 (Leela Chess Zero)](https://lczero.org/),
  [GNU Chess](https://www.gnu.org/software/chess/),
  [Fire](https://github.com/FireFather/fire/),
  [Maia Chess](https://maiachess.com/), and PyChess itself supplies its own chess
  engine.

## Disclaimer

Stockfish already ships with Fedora and most other Linux distributions, but
those vendor-supplied versions are usually woefully out of date. Therefore, I
offer this build for your own convenience. I make no guarantee that it works as
it should. Buyer beware. :) I am in no way affiliated with the developers of
Stockfish, but I do thank them and the larger Stockfish community who have made
incredible chess engine possible.

# Questions or comments&nbsp;.&nbsp;.&nbsp;.

Contact: **t0dd_at_protonmail.com** or find me at **@t0dd:matrix.org** in the [Matrix](https://github.com/taw00/element-rpm) social medias.
