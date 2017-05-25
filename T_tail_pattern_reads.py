file_in="/Users/damirvana/Desktop/Uli_script_Python/257840-257900_reads.fasta"           
file_out="/Users/damirvana/Desktop/Uli_script_Python/T-tail_file_out_new.csv"  

def TTailSearch(file_in,file_out):
    '''
    search for pattern of >=10 nucleotides (any) followed by >=16 T nucleotides and >=10 nucleotides (any) 
    in sequencing reads. For any match write T-tail length/start and end coordinate of T-tail/ length of downstream and 
    upstream flanking sequences/sequence of read in csv file  
    
    e.g match: ATAGAATAAAGATCCTTTACTTTATTAATTGTTTTAAAAAGTAACTTTGTTACTTAATTAAACGCTTTTCATTTTTTTTTTTTTTTTTGAATTTGCGAAA
    '''
    
    import csv
    import re
    # define regular expression search pattern
    T_tail = re.compile(r"\w{10,}[T]{16,}\G\w{9,}")
    
    with open(file_out,"w") as f_out:
    
        colnames=["length T-tail","start coordinate T-tail", "end coordinate T-tail", "length upstream seq", "length downstream seq", "read"]
        out_writer=csv.DictWriter(f_out,fieldnames=colnames)
        out_writer.writeheader()
      
        with open(file_in,"r") as f_in:
            in_reader=csv.reader(f_in)
            summary_dict={}
            for row in in_reader:
                # > in line denotes read ID
                if row[0][0] != ">":
                    read = row[0]
                    T_tail_match = T_tail.search(read)
                    if T_tail_match:
                        # use re to return coordinates of T_tail
                        T_tail_coordinates = re.search(r"[T]{16,}", T_tail_match.group()).span()
                        T_tail_length = T_tail_coordinates[1]-T_tail_coordinates[0]
                        length_downstream_seq = len(T_tail_match.group())-T_tail_coordinates[1]
                        
                        summary_dict["length T-tail"]= T_tail_length
                        summary_dict["start coordinate T-tail"]=T_tail_coordinates[0]+1 # corrects for python starting counting at 0
                        summary_dict["end coordinate T-tail"]=T_tail_coordinates[1] 
                        summary_dict["length downstream seq"]=length_downstream_seq
                        summary_dict["length upstream seq"]=T_tail_coordinates[0]    
                        summary_dict["read"]=read
            
                       
                        out_writer.writerow(summary_dict)