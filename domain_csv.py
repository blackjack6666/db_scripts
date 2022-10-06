import numpy as np
import pandas as pd
import json
import pickle
ptm_map_dict = {'Q\\[129\\]':'Gln deamidation','N\\[115\\]':'ASN deamidation',
                'Q\\[111\\]':'Gln to pyroGln','C\\[143\\]':'selenocysteine',
                'M\\[15\\.9949\\]':'Met oxidation','P\\[15\\.9949\\]':'Pro hydroxylation',
                'K\\[15\\.9949\\]':'Lys hydroxylation','n\\[42\\.0106\\]':'N-term acetylation',
                'C\\[57\\.0215\\]':'Cys redu-alky','R\\[0\\.9840\\]':'Arg deamidation','Y\\[79\\.9663\\]':'Phospho-Tyr',
                'T\\[79\\.9663\\]':'Phospho-Thr', 'S\\[79\\.9663\\]':'Phospho-Ser'}


def domain_cov_ptm_csv(prot_freq_dict, ptm_map_result, domain_pos_dict,protein_entry:str,output_name):
    """
    -----
    output CSVs for domain coverage and domain ptms
    :param prot_freq_dict:
    :param ptm_map_result:
    :param domain_pos_dict:
    :param protein_entry:
    :return:
    """

    if protein_entry not in domain_pos_dict:
        return f'{protein_entry} no SMART domain available'
    else:
        freq_array = prot_freq_dict[protein_entry]
        domain_dict = domain_pos_dict[protein_entry]
        ptm_index_dict = ptm_map_result[protein_entry]
        info_list = []
        ptm_info_list = []
        for each_domain in domain_dict:
            for each_tp in domain_dict[each_domain]:
                start, end = each_tp[0], each_tp[1]
                # calculate domain coverage
                coverage = np.count_nonzero(freq_array[start - 1:end]) / (end - start + 1)*100
                info_list.append([start, end, coverage, each_domain])
                # domain ptms
                for ptm in ptm_index_dict:
                    ptm_index_ary = ptm_index_dict[ptm]
                    domain_ptm_idx = np.where((ptm_index_ary>=start-1)&(ptm_index_ary<=end-1),ptm_index_ary,0)
                    ptm_info_list.append([start,end,ptm_map_dict[ptm],np.array2string(domain_ptm_idx[domain_ptm_idx!=0]+1,separator=', ')[1:-1],each_domain])
        if info_list == []:
            return f'{protein_entry} no SMART domain available'
        else:
            df_cov = pd.DataFrame(info_list,columns=['start','end','seq cov%','domain name'])
            df_ptm = pd.DataFrame(ptm_info_list,columns=['start','end','PTM','position','domain name'])
            df_cov.to_csv(output_name+'_DomainCov.csv')
            df_ptm.to_csv(output_name+'_DomainPTM.csv')


if __name__=='__main__':
    with open('F:/matrisomedb2.0/smart_domain_0908.json') as f_o:
        info_dict = json.load(f_o)

    ## domain cov/PTM CSVs
    folder = 'F:/matrisomedb2_0_revise/domain_cov_ptm_csv/'
    ## global data
    # glob_prot_freq_dict = pickle.load(open('F:/matrisomedb2.0/glob_prot_freq_dict.p', 'rb'))
    # glob_ptm_map = pickle.load(open('F:/matrisomedb2.0/glob_prot_ptm_ind_dict.p','rb'))
    # for prot in glob_prot_freq_dict:
    #     print (prot)
    #     domain_cov_ptm_csv(glob_prot_freq_dict,glob_ptm_map,info_dict,prot,folder+prot)

    ## sample data
    sample_data = pickle.load(open('F:/matrisomedb2_0_revise/sample_result9.data', 'rb'))
    for sample in sample_data:
        print(sample)
        prot_freq_dict, ptm_map = sample_data[sample]['freq'], sample_data[sample]['ptm']
        for prot in prot_freq_dict:
            domain_cov_ptm_csv(prot_freq_dict, ptm_map, info_dict, prot,
                                folder + sample.replace('/', '_').replace('\u0394', '') + '_' + prot)
