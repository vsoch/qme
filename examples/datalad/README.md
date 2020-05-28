### Datalad

[Datalad](http://docs.datalad.org/en/stable/generated/man/datalad-run.html) is a tool
for managing local and remote datasets. QueueMe has a wrapper for the `datalad run`
command. Note that you will need to install both DataLad and git-annex, and 
instructions are provided [here](http://handbook.datalad.org/en/latest/intro/installation.html).
On Ubuntu that looks like this:

```bash
pip install datalad
```

Git annex was harder, the standard `apt-get install -y git-annex` didn't work.
I needed to install from [neurodebian](http://neuro.debian.net/install_pkg.html?p=git-annex-standalone)

```bash
wget -O- http://neuro.debian.net/lists/bionic.us-nh.libre | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
sudo apt-key adv --recv-keys --keyserver hkp://pool.sks-keyservers.net:80 0xA5D32F012649A5A9
```

then update and install:

```bash
sudo apt-get update
sudo apt-get install git-annex-standalone
```

## 1. Create a Dataset
Next, let's create a folder for a fun dataset. We will download a pokemon 
database.

```bash
git clone https://github.com/vsoch/pokemon
```

And let's get rid of everything except for the data.

```bash
$ mv pokemon/pokemon/database ./database
$ rm -rf pokemon/
$ ls
database  README.md
```

Great! Now we will use datalad to create a database. We use the `--force` option
because we are creating one in a folder that already exists.

```
$ datalad create --force database
[INFO   ] Creating a new annex repo at /home/vanessa/Desktop/Code/qme/examples/datalad/database 
create(ok): /home/vanessa/Desktop/Code/qme/examples/datalad/database (dataset)
```

What is actually happening? It's creating a hidden `.datalad` folder there with 
a configuration.

```bash
$ cat database/.datalad/config 
[datalad "dataset"]
	id = 9475829a-a100-11ea-a718-dd731a289e9e
```
We will start with the tutorial [here](http://handbook.datalad.org/en/latest/basics/101-108-run.html)
to set up a repository and run a command, and then do it with QueueMe.


## 2. Save your Dataset

The simplest thing we can do is run `datalad save` to save our dataset. So change directory
into the database, and do that.

```bash
$ cd database/
$ datalad save
add(ok): images/1.jpg (file)                                                                                                    
add(ok): images/10.jpg (file)
add(ok): images/100.jpg (file)
add(ok): images/101.jpg (file)
add(ok): images/102.jpg (file)
add(ok): images/103.jpg (file)
add(ok): images/104.jpg (file)
add(ok): images/105.jpg (file)
...
add(ok): images/99.jpg (file)
add(ok): pokemons.json (file)
save(ok): . (dataset)
action summary:
  add (ok: 891)
  save (ok: 1)
(base) vanessa@vanessa-ThinkPad-T490s:~/Desktop/Code/qme/examples/datalad/database$ datalad save
```

## 3. Update or Change your Dataset

Great! At this point we might [publish or otherwise move the dataset around](http://handbook.datalad.org/en/latest/intro/executive_summary.html#consumption-and-collaboration), but instead we are going
to use [datalad run](http://handbook.datalad.org/en/latest/basics/101-108-run.html).
The basic idea of datalad run is that when we run some command on a dataset to change or
otherwise update it, we want to keep this metadata somewhere. So let's say that we run a command
to list the sorted weights of our pokemons:

```bash
$ cat pokemons.json | jq '.[].weight' | sort --reverse -n
2204.4
2204.4
2094.4
2094.4
2028.3
1957.7
1807.8
1763.7
1730.6
1653.5
1505.8
1433
1212.5
...
0.2
0.2
0.2
0.2
0.2
```

Wow, we really got some chonkers! Now let's save this to an output file.

```bash
$ cat pokemons.json | jq '.[].weight' | sort --reverse -n --output fatties.txt
```

What we've just done is created a new file for our dataset! We can use `datalad status`
to see that it's not officially added:

```bash
$ datalad status
untracked: fatties.txt (file)
```

We can now save the file to our dataset. This time we will use a message with `-m`.

```bash
$ datalad save -m "Adding fatties.txt file, a descending sorted list of pokemon weights."
add(ok): fatties.txt (file)
save(ok): . (dataset)
action summary:
  add (ok: 1)
  save (ok: 1)
```

## 4. Datalad Run

Now we are ready for datalad run. The basic idea is that, let's say that some time
passed, and we want to update our fatties.txt file. If we run the command without datalad run
we would get the changed file and could update the git history, but what we really want to
do is also save the command that we used to make that update! Let's give that a go!

```bash
$ datalad run -m "updating fatties.txt" "rm fatties.txt && cat pokemons.json | jq '.[].weight' | sort --reverse -n --output fatties.txt"
[INFO   ] == Command start (output follows) ===== 
[INFO   ] == Command exit (modification check follows) ===== 
add(ok): fatties.txt (file)
action summary:
  add (ok: 1)
  save (notneeded: 1)
```
And then importantly, the metadata we need to reproduce the command is in our git history:

```bash
$ git log
commit bf842cc743af0bcc83b8db6523e43d196957fb3e (HEAD -> master)
Author: vsoch <vsochat@stanford.edu>
Date:   Thu May 28 11:00:58 2020 -0600

    [DATALAD RUNCMD] updating fatties.txt
    
    === Do not change lines below ===
    {
     "chain": [],
     "cmd": "rm fatties.txt && cat pokemons.json | jq '.[].weight' | sort --reverse -n --output fatties.txt",
     "dsid": "9475829a-a100-11ea-a718-dd731a289e9e",
     "exit": 0,
     "extra_inputs": [],
     "inputs": [],
     "outputs": [],
     "pwd": "."
    }
    ^^^ Do not change lines above ^^^
```

Next, let's discuss how we can interact with QueueMe.
