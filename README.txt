The repository contains the scripts that have been used for the Community detection project.

The files named point_LINKNAME.py contain the definition of the Point class for several kinds of links and the definition of the DBSCAN class. In order to create other links, one has to create a new Point class.

The files named edges_LINKNAME.py import point_LINKNAME.py as modules and compute the links of type LINKNAME for a given subset of the dataset. They are all used with the following command:

./edges_LINKNAME.py cftable nproc output_file

where cftable is the file which defines the subset of the dataset. It is obtained by the original file soggetti_an.csv. The original file is filtered according to the column DATA_INSERIMENTO as needed, then the file obtained is modified so that for each line it only contains the following: ID_SOGGETTO ID_CF. Examples of such tables are in /lustre/mhpc/mhpc04/generali, all named cftable_*.
nproc indicates the number of processes we want to use, and output_file is the name of the file that will contain the edges after the program has run, and will be used by the second Python script.

The files named edges_LINKNAME_split.py import point_LINKNAME.py as modules and compute the links of type LINKNAME between two given subsets of the dataset (that is, the links of the kind (node1, node2) where node1 belongs to the first subset and node2 to the second). They are all used with the following command:

./edges_LINKNAME_split.py cftable1 nproc cftable2 output_file

The scripts of the form edges_LINKNAME.py and edges_LINKNAME_split.py also read other files as input, which are hardcoded. They are all in /lustre/mhpc/mhpc04/generali, and for the links we already worked on, they are the following:

soggetti_an.csv
e_mail_id.csv
ccred_an.csv
link_pre_veicoli_an.csv
preventivi_an.csv
rolestable
true_plates_table

The files named label_prop_* and dbscan_* compute Table 1 and Table 4, after applying label propagation or DBSCAN respectively. They are all used with the following command:

./ALGORITHM_TABLE.py cftable nproc edges_file output_file 

where edges_file is the file which has been output by the first Python script, or a merge of files of that kind, in case one wants to run with over 1M customers.
