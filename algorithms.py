#The following are a set of algorithms I have written to resolve a variety of dilemmas posed online.
#They are for personal growth only.

def minimumBribes(q):
    
    #The following algorithm determines the minimum number of permutations
    #of a list in order to achieve a current state originating from an ordered array.

    base_lst=[i+1 for i in range(len(q))]
    original_inds = {item:i for i,item in enumerate(base_lst)}
    end_inds = {item:i for i,item in enumerate(q)}

    pos_count=0
    neg_count=0
    zer_count=0
    
    final_count=0
    
    ind_lst=list()

    for entry in q:
        ind_dif = original_inds[entry] - end_inds[entry]
        print(entry, ind_dif)
        if ind_dif > 2:
            print('Too chaotic')
            return None
        if ind_dif <= 0:
            continue
            
        final_count+=ind_dif
        ind_lst.append(ind_dif)

    ret_val = int(final_count)
    print(ret_val)


def climbingLeaderboard2(scores, alice):
    
    #this algorithm analyzes movement of numerical values in an array. 
    
    result=list()
    alice = sorted(alice)
    scores=sorted(list(set(list(scores))))
    placeholder=0
    len_scores=len(scores)
    test_dict=dict()

    for al_score in alice:
        #print(al_score)
        for i in range(placeholder, len_scores):
            score=scores[i]
            #print(i, al_score, score)
            if i == 0 and al_score <= score:
                test_dict[al_score]=i+1
                result.append(i+1)
                placeholder = i+1
                break
            elif al_score > score:
                test_dict[al_score]=i+2
                result.append(i+2)
                placeholder=i+2
                break
            elif al_score == score:
                test_dict[al_score]=i+1
                result.append(i+1)
                placeholder=i+1
                break
            else:
                continue

    return test_dict        
    return sorted(result, reverse=True)


def extra_long_factorials(n):
    #this simple algorithm calculates factorials
    to_multiply = list(range(1, n+1))
    result=1
    for number in to_multiply:
        result = result*number
    print(result)
    

three_lists = [[4,9,2],[3,5,7],[6,4,2]]

def magic_square(three_lists):
    
    #The following function takes a square matrix and determines the minimal 'cost' necessary to
    #produce a magic square matrix, characterized by all columns, rows and diagonals adding up
    #to the same number. It achieves this by taking the input, producing all possible permutations
    #of the matrix, singling out magic matrices and then analyzing the cost of each magic matrix
    #concluding, which one has the least cost.
    
    input_array = np.array(three_lists)
    shape_tup = input_array.shape
    howmanynums = shape_tup[0] * shape_tup[1]
    to_sample = list(range(1,howmanynums+1))
    index_dict=dict()
    
    for row_ind, row_val in enumerate(input_array):
        for col_ind, col_val in enumerate(input_array):
            index_dict[(row_ind, col_ind)]=input_array[row_ind, col_ind]
    
    perms = it.permutations(to_sample)
    
    all_arrays=[]
    for perm in perms:
        perm=list(perm)
        all_arrays.append(np.array(perm).reshape(shape_tup))
    magic_arrays=[]
    how_many=shape_tup[0]
    
    for ar in all_arrays:

        sums=set()
        diag1=[]
        diag2=[]
        for i, row in enumerate(ar):
            sums.add(sum(row))
            diag1.append(row[i])
            diag2.append(row[(i+1)*-1])
        if len(sums) > 1:
            continue
        for i, row in enumerate(ar.T):
            sums.add(sum(row))
        sums.add(sum(diag1))
        sums.add(sum(diag2))
        if len(sums) > 1:
            continue
        magic_arrays.append(ar)
        
        
    costs=[]
    
    for magic_array in magic_arrays:
        local_total=0
        for ind in index_dict:
            local_cost = abs(magic_array[ind] - input_array[ind])
            local_total+=local_cost
        costs.append(local_total)
    print(min(costs))
            

def make_substrings(input_word, second=False):
    
    #the following algorithm is a subcomponent of the following one in order to determine all
    #substrings in a given string.
    
    if second:
        input_word=input_word[0]

    all_substrings=[]
    wd_length = len(input_word)
    base_inds = list(range(wd_length))

    for i in base_inds:
        substring_inds = list(range(i, wd_length))
        substring=''
        for ind in substring_inds:
            substring+=input_word[ind]
        all_substrings.append((substring, i))

    for i in base_inds:
        substring_inds = list(range(0,i))
        substring=''
        for ind in substring_inds:
            substring+=input_word[ind]
        all_substrings.append((substring, i))

    return all_substrings


def find_substrings(substrings_lst):
    
    inter_lst=list()
    ret_lst=list()
    
    for sub in substrings_lst:
        to_add = make_substrings(sub, second=True)
        inter_lst.append(to_add)
        
    for item in inter_lst:
        for substring in item:
            if len(substring) < 1:
                continue
            ret_lst.append(substring)
    ret_lst = sorted([item[0] for item in ret_lst if len(item[0]) > 0], key = lambda x: len(x))
        
    return set(ret_lst)

substrings = find_substrings(make_substrings('abracadabra'))

def get_all(substrings, word):
    
    #the following function uses the above function to find all substrings of a series of original substrings,
    #outputting a master list of substrings.
    all_lst=list()
    for item in substrings:
        all_lst.append(item)
        count=0
        for i in range(len(word)-len(item)+1):
            if word[i:len(item)+i] == item:
                count+=1
                if count > 1:
                    all_lst.append(item)
    return sorted(all_lst, key = lambda x: len(x))
                
all_substrings = get_all(substrings, 'abracadabra')

def get_palindromes(all_substrings):
    
    #the following algorithm determines the number of "palindromic borders" in an original word
    #by analyzing all borders in all substrings to determine whether or not they are palindromic.
    #The overall algorithm consisting of these three last functions define substrings as
    #slices of a string that are distinct or that occur at different positions within the original word.

    count=0
    sup_set=set()
    for entry in all_substrings:
        sup_set.add(entry)
        for i in range(len(entry)):
            b1 = entry[:i]
            b2 = entry[-1*i:]
            if b1 == b2:
                newb2=''
                for i in range(1,len(b2)+1):
                    newb2+=b2[-1*i]
                if b2 == newb2:
                    count+=1
                    borders=(b1, newb2)
                    print(entry, borders)


    return count

to_ret=get_palindromes(all_substrings)
print(to_ret)
            
