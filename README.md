# Stockfish — a powerful open-source chess engine

_.&nbsp;.&nbsp;.&nbsp;packaged for Fedora, CentOS, and OpenSUSE_

Stockfish is a free UCI chess engine derived from Glaurung 2.1. It is not a
complete chess program, but requires a UCI-compatible graphical user interface
(GUI) (e.g. PyChess, XBoard with PolyGlot, Scid, Cute Chess, eboard, Arena,
Sigma Chess, Shredder, Chess Partner or Fritz) in order to be used comfortably.
Read the documentation for your GUI of choice for information about how to use
Stockfish with it.

Stockfish, in recent years, has topped the list of strongest chess engines ever
developed. But it can be used by weak players like myself as well to learn and
analyze or just to have fun playing a game. PyChess, which I keep recommending,
allows you to tone down Stockfish's capabilities to bludgeon you to death with
chess logic. :)

_**What is this GitHub Repository?**_

The purpose of this repository is to store all the bits and pieces needed to
build and package this application for various RPM flavors of Linux. The binary
(installable and runnable) packages are then built via the [Fedora Project's
COPR build system](https://copr.fedorainfracloud.org/coprs/taw/stockfish/).
Note, core upstream code—for example, `Stockfish-sf_14.tar.gz`—will not be
redundantly stored here. Those can be found ... up stream. What is stored in
this repository are the _unique_ bits needed to build a source RPM—i.e., all
the things I add, or find convenient to track within this repository. If you
know your way around building RPMs, you will know how to work with specfile and
sources found here.

#### More about&nbsp;.&nbsp;.&nbsp;.

* Stockfish: <https://stockfishchess.org/>
* PyChess: <https://pychess.github.io/>, an excellent open-source chess frontend that can use Stockfish — recommend

# tl;dr&nbsp;.&nbsp;.&nbsp;.

## I just want to install Stockfish and play chess (using PyChess in this example)!

### [Fedora and CentOS]

**Prep&nbsp;.&nbsp;.&nbsp;.**
```bash
sudo dnf install -y dnf-plugins-core distribution-gpg-keys
sudo dnf copr enable taw/stockfish
```

**Install&nbsp;.&nbsp;.&nbsp;.**
```bash
sudo dnf install -y stockfish pychess --refresh
```

### [OpenSUSE]

**Prep (Leap 15.X)&nbsp;.&nbsp;.&nbsp;.**
```bash
# Install GPG keys
sudo rpm --import https://keybase.io/toddwarner/key.asc
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
```bash
# Install GPG keys
sudo rpm --import https://keybase.io/toddwarner/key.asc
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
sudo zypper install stockfish pychess
```

## I installed it, now I want to play a game!

1. Open PyChess via your application menus.
2. Select a color for yourself and select Stockfish as your opponent
3. Play chess!

# Disclaimer

I developed this packaging for my own use and because the officially shipped
builds are usually woefully behind. I offer these builds for your own
convenience. I make no guarantee it works as it should. Buyer beware. :) I am
in no way affiliated with the originators of Stockfish—but I do thank them and
the larger community of developers who have made it all possible—for this
incredible chess engine.

# Questions or comments&nbsp;.&nbsp;.&nbsp;.

Contact: **t0dd_at_protonmail.com** or find me at **@t0dd:matrix.org** in the Matrix / Element social medias.
