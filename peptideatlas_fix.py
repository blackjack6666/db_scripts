from glob import glob
import json
import re
from collections import defaultdict

mouse_uniprotids = {'Q60736', 'Q9R157', 'Q9R1N9', 'Q9R1V4', 'P35174', 'Q3U492', 'Q9D7P9', 'Q99MQ5', 'Q91YE3', 'Q9JM84', 'Q8JZM8', 'P14097', 'P55066', 'Q7TS55', 'P04095', 'Q8C6K9', 'Q9JI76', 'Q9R171', 'O70283', 'Q8K4G2', 'P50114', 'A2AX52', 'Q8K410', 'P21460', 'P70207', 'Q8CGZ9', 'Q9JHG0', 'Q62507', 'Q9DC11', 'Q6IR41', 'P07759', 'Q02496', 'Q8CIZ8', 'Q8VCS3', 'P29621', 'Q60994', 'P10148', 'O08665', 'A6X935', 'Q9JHB3', 'P35173', 'Q3U435', 'Q9Z123', 'Q2VIS4', 'Q9WUA1', 'Q8CAL5', 'O35988', 'P18828', 'Q64280', 'Q8C8T7', 'O08677', 'O89029', 'Q7TMJ8', 'Q9ESM3', 'Q8R4K8', 'Q91VD1', 'Q8K3F2', 'P97821', 'Q9DAS4', 'P50404', 'Q8BUE7', 'P54615', 'Q00897', 'Q9ESN4', 'Q9Z0H6', 'P09920', 'P70389', 'P61329', 'A2AED3', 'Q640N1', 'P18242', 'P70275', 'P17515', 'P28825', 'Q68SA9', 'Q99KC8', 'P47876', 'Q9R0M3', 'Q8CI19', 'Q6DFY8', 'P10168', 'Q8R534', 'Q61001', 'Q9WTR0', 'P56677', 'P43028', 'Q9WVJ9', 'Q05910', 'P22777', 'Q01149', 'P07349', 'Q07643', 'Q6W3F0', 'Q60841', 'Q71M36', 'Q2VWQ2', 'P41160', 'O55189', 'P09225', 'O55038', 'Q62356', 'P51942', 'Q8CJH3', 'P23359', 'Q8BHE5', 'Q9D3P1', 'P36363', 'P58459', 'Q80UG2', 'Q3UR50', 'O54693', 'Q9CQ76', 'O09126', 'Q684R7', 'Q9Z126', 'P10889', 'P10749', 'Q9WV56', 'Q9JII2', 'Q923D3', 'Q60847', 'Q3UP87', 'Q68FM6', 'Q8BFU0', 'Q9D1D6', 'A2AVA0', 'B2RXS4', 'Q8K1S1', 'Q9Z2H6', 'Q811Q4', 'P20181', 'P70375', 'P10761', 'O55226', 'Q8CG19', 'P39876', 'Q8CEK3', 'O35640', 'P01132', 'O55225', 'F8VQ03', 'P10493', 'Q6NZL8', 'Q8C1T8', 'P04351', 'P10923', 'Q4VBE4', 'Q501P1', 'Q8R0Z6', 'P49300', 'Q6DFV8', 'P24383', 'P48030', 'Q70UZ7', 'P47880', 'P32972', 'O54974', 'Q61292', 'Q9QUR8', 'Q9JHK0', 'Q9JHH5', 'P43431', 'Q61247', 'Q61521', 'Q9CQ04', 'Q9QZZ6', 'P98064', 'Q60715', 'Q7TSK7', 'P21841', 'Q80Z71', 'P21274', 'P11403', 'Q9Z0L4', 'Q2UY11', 'P01326', 'Q5I2A0', 'P09586', 'Q91VF5', 'Q8K419', 'P12032', 'P59509', 'Q07456', 'O08859', 'O09037', 'P11859', 'Q91WP0', 'Q4ZJM9', 'Q9ER58', 'Q5SV42', 'P14069', 'Q504P2', 'Q8BPB5', 'Q60813', 'Q60571', 'Q7TQN3', 'Q80X19', 'P37889', 'Q9JM99', 'Q9Z1T2', 'P05524', 'Q9R0S2', 'O35227', 'Q9JJZ5', 'Q62177', 'O70300', 'Q61282', 'Q8BWY2', 'P50592', 'P48615', 'Q05793', 'P11087', 'Q9QY05', 'Q61592', 'Q8BVD7', 'Q64739', 'Q9D1H9', 'P28301', 'Q8BMF8', 'Q9R014', 'P20109', 'Q8BGZ8', 'C0HKD9', 'Q9EQC7', 'P70377', 'Q61072', 'P97347', 'Q00780', 'A9Z1V5', 'P59900', 'Q3UPR9', 'Q62000', 'O88676', 'P01325', 'P07141', 'Q05895', 'Q80YX1', 'Q9EQ14', 'P97299', 'Q5MJS3', 'Q91XD7', 'P70208', 'Q9Z0E2', 'O70326', 'Q61398', 'Q6P3Y9', 'P21275', 'P19788', 'P02463', 'Q8R4G0', 'O09049', 'P04768', 'Q62181', 'Q8R1R4', 'Q9D7I9', 'Q9DBB9', 'Q4LFA9', 'P07321', 'Q8CFR0', 'Q9JK88', 'Q08879', 'Q7TQ62', 'Q9CYA0', 'E9PV24', 'P20033', 'Q8K406', 'O88947', 'Q05306', 'P31725', 'Q8R054', 'Q8VHP7', 'O35257', 'P05017', 'P57110', 'Q64519', 'Q6HA09', 'P86793', 'P01575', 'P35441', 'P13609', 'Q9JI78', 'Q9R182', 'P11276', 'Q811B3', 'Q8BLI0', 'Q925S4', 'Q9WUH7', 'P97298', 'Q922T2', 'P20239', 'Q5QNQ9', 'P55097', 'O35188', 'O09107', 'Q80ZF2', 'Q10738', 'P32261', 'O54951', 'P58022', 'A2ASQ1', 'Q9CQW5', 'P20722', 'P51655', 'O89098', 'P37237', 'Q03350', 'Q8BLY1', 'P50543', 'P35242', 'Q04998', 'O54830', 'Q60997', 'Q9D1U0', 'P02468', 'P25785', 'Q8BLX7', 'P97400', 'Q9R087', 'O54732', 'Q80XD9', 'P21658', 'P49764', 'P41155', 'P51642', 'Q9D7D2', 'Q8K482', 'Q9R007', 'Q9R1V7', 'O35622', 'O08800', 'P70380', 'Q8R066', 'Q8R1Q3', 'P97463', 'P70194', 'Q9D8U4', 'Q9WVH9', 'Q8BNJ2', 'O35228', 'Q8CGD2', 'P97953', 'P15656', 'P20918', 'P61148', 'P01139', 'Q8R0S6', 'Q8VEA6', 'Q91X72', 'Q9R159', 'Q8CDC0', 'O35565', 'Q9ESL9', 'Q3TTE0', 'Q62226', 'Q8BG58', 'P54130', 'Q61716', 'Q9WU66', 'A2AJ76', 'Q8CID3', 'P29788', 'Q8VCD3', 'O54831', 'Q60753', 'Q62179', 'P97927', 'Q8VCC9', 'Q91ZJ9', 'Q9JLF6', 'P07350', 'Q9D968', 'E9Q7T7', 'Q9EPW4', 'Q9CQ58', 'Q9D269', 'Q8K0D2', 'Q66PY1', 'Q07968', 'P05208', 'Q8K4Z0', 'Q0Q236', 'Q8CJ91', 'P70663', 'Q6P4P1', 'P34960', 'P54320', 'Q9QZS0', 'P18121', 'P19467', 'P60882', 'Q91UZ4', 'O70138', 'Q9JM58', 'P55105', 'Q924X1', 'O55188', 'Q4ZJN1', 'P53690', 'P70379', 'Q61220', 'Q9CQ52', 'P28481', 'P22599', 'O89093', 'P01586', 'O88839', 'Q8BMS2', 'Q7TNI7', 'Q6NVD0', 'Q9D2H8', 'Q8R422', 'Q91V08', 'P43407', 'Q8K4Q8', 'Q80T91', 'P18893', 'Q8BZH1', 'Q8BJ73', 'Q9JK53', 'Q30D77', 'P97290', 'Q149M0', 'Q505H4', 'Q3UQ22', 'Q9QXT6', 'Q9QYS1', 'Q8K007', 'P21237', 'Q8BRU4', 'O35206', 'Q5H8B9', 'Q924C6', 'Q62381', 'Q9Z1W4', 'Q9D708', 'Q8BH34', 'Q07104', 'Q5FW85', 'Q62386', 'P43027', 'Q9D0F3', 'Q9D676', 'P63075', 'Q6JHY2', 'P28666', 'O89101', 'P06869', 'Q91ZW8', 'P08505', 'P10855', 'P27106', 'P40226', 'P04426', 'Q9R0Q8', 'P17125', 'Q91WP6', 'P50228', 'Q60675', 'Q9ESB3', 'Q8BQH6', 'P21956', 'P49766', 'P97401', 'O88992', 'P08122', 'P15247', 'Q8BH27', 'Q9Z175', 'P48540', 'Q61847', 'Q9R0G6', 'Q76KF0', 'O88322', 'P25318', 'Q9CRB5', 'Q61191', 'P14106', 'P28047', 'Q9Z0J7', 'Q9ESS2', 'E9PXB6', 'Q9WUD6', 'Q8BME9', 'Q99JG3', 'O54907', 'Q2TJ95', 'Q3UVV9', 'Q8K4L6', 'Q9R1A3', 'Q80Y72', 'P04202', 'P82198', 'Q64527', 'P16045', 'P27784', 'Q8K4C5', 'Q8K479', 'P70378', 'Q9JLV9', 'P97399', 'Q8K4G1', 'Q80X76', 'Q6PZE0', 'O08524', 'O35608', 'Q9QZC2', 'Q9WVH6', 'O88207', 'P97873', 'Q4VC17', 'O54824', 'P48794', 'Q9QYH9', 'Q04997', 'P02469', 'Q63870', 'O35367', 'Q91VF6', 'Q923W9', 'P97429', 'Q8R4W6', 'Q80TR4', 'Q923P0', 'O08523', 'Q05928', 'P56565', 'Q4ZJM7', 'Q9R158', 'Q80WM5', 'Q91V88', 'O08762', 'Q9R0X2', 'J3S6Y1', 'Q9D695', 'Q8C8N3', 'P10146', 'Q7TN16', 'Q91ZF2', 'Q6W5C0', 'Q8CF98', 'P39061', 'Q9R0S3', 'Q3UQ28', 'P40224', 'Q02105', 'Q61824', 'Q80ZN5', 'O54891', 'Q9WU72', 'Q07079', 'Q9D236', 'P06799', 'Q61087', 'P25085', 'Q8BKV0', 'Q9ES30', 'P30882', 'Q9QXP7', 'Q9WVM6', 'P35419', 'P55104', 'Q7TMF5', 'P41317', 'Q0VF58', 'Q9WVF9', 'Q05A56', 'Q8C8H8', 'P12388', 'P70269', 'O35903', 'Q8VEI3', 'Q9Z0F8', 'P43021', 'Q00896', 'Q9D2Q8', 'Q7TSQ1', 'P83503', 'P63089', 'Q812F3', 'Q91X79', 'O35684', 'Q9WTX4', 'Q99JR5', 'P26928', 'Q9R045', 'Q8CIE0', 'P16110', 'Q9R0B6', 'O08746', 'P86547', 'Q61810', 'Q9QZF2', 'C0HKD8', 'Q9D8G5', 'P21552', 'Q3UW26', 'P47931', 'P48298', 'Q62217', 'P48036', 'P47873', 'P97857', 'Q62059', 'O35474', 'O35181', 'Q8BJ66', 'Q9QUN5', 'P01587', 'P07091', 'Q8C6Z1', 'Q80SU4', 'Q91YE2', 'Q8R4F1', 'P35230', 'Q07235', 'Q9D154', 'Q8K0E8', 'P16675', 'Q61789', 'Q9JHI0', 'Q02788', 'Q9JIA9', 'O35348', 'Q920C1', 'Q9Z132', 'P33435', 'Q9R098', 'P47878', 'Q6GUQ1', 'Q8VHY0', 'Q9WVL7', 'P21981', 'Q9QZR9', 'Q9R1B9', 'O08538', 'Q91ZX1', 'O70460', 'Q9JJN1', 'P48614', 'Q04592', 'Q9R0B9', 'B2RY83', 'Q03366', 'Q3U0K8', 'P07750', 'P97812', 'Q8CFG0', 'Q9WUQ5', 'P97352', 'Q61838', 'Q8BNX1', 'Q9JIL2', 'Q80W15', 'O88430', 'O35256', 'P43025', 'P09535', 'P20863', 'P06879', 'O35468', 'P57748', 'Q62288', 'P19137', 'Q9JL95', 'P56203', 'Q61361', 'Q8R4V5', 'Q8C088', 'O88200', 'Q60519', 'Q8BGU2', 'Q9QUP5', 'P14824', 'Q80WM4', 'P12804', 'Q9QZ10', 'Q8VHI5', 'P86792', 'Q8CG65', 'Q05722', 'Q61703', 'Q62426', 'Q9R0E1', 'Q8BH61', 'P07146', 'Q00731', 'O09118', 'Q9Z1P8', 'P28653', 'P04769', 'D3YXG0', 'Q9R160', 'P61939', 'O35235', 'P07214', 'Q99K41', 'P06797', 'Q9JL96', 'A2RT60', 'P10605', 'Q61554', 'Q07076', 'Q61508', 'B2RPV6', 'Q62401', 'Q9R001', 'P84444', 'Q9R118', 'P31240', 'O70514', 'Q71KU9', 'P28654', 'Q08048', 'Q99MQ4', 'Q9R0H2', 'Q9Z121', 'Q64151', 'Q8K1K6', 'Q769J6', 'Q9JHA8', 'P50608', 'P22724', 'Q04999', 'P51865', 'Q9WVB4', 'Q9JHQ0', 'P49182', 'Q6QLQ4', 'Q69Z28', 'Q80T14', 'Q3V1M1', 'P70186', 'Q61555', 'Q61581', 'Q9ESL8', 'P97435', 'Q9R0E2', 'Q80YC5', 'Q9QZM3', 'Q9Z0L2', 'Q9EPX2', 'Q9JL15', 'P41274', 'Q9JI81', 'P06804', 'Q02853', 'Q8C119', 'Q03734', 'Q9JKC0', 'Q8R1W8', 'Q9EPL5', 'Q920A0', 'Q9R013', 'Q9R229', 'O08689', 'Q9QZJ6', 'P62818', 'Q8CFZ4', 'Q61711', 'P51885', 'P97384', 'P22727', 'P53347', 'P70701', 'Q9JIA1', 'O88310', 'Q8BZQ2', 'P70124', 'Q62010', 'P35175', 'A6H6E2', 'P07356', 'Q3UH93', 'P11214', 'Q62009', 'P97816', 'Q80V70', 'Q00898', 'Q9JLL0', 'Q9EPL6', 'P19221', 'P56974', 'Q8BYI9', 'P70458', 'Q8R121', 'O08999', 'Q9DAY2', 'P49935', 'P97766', 'Q8R5M2', 'P63084', 'Q08189', 'Q9JLN6', 'Q8VED9', 'Q61488', 'Q9JJS0', 'Q8BKV1', 'Q61702', 'O08717', 'Q6YGZ1', 'Q5UBV8', 'Q8BJD1', 'Q9EPC2', 'P98063', 'Q07563', 'P22726', 'Q1HCM0', 'P22725', 'P28862', 'P83714', 'P43029', 'Q61704', 'Q9WTM3', 'Q9Z1N6', 'Q80XH2', 'P12025', 'P01580', 'P07351', 'Q06770', 'Q9JI33', 'Q60718', 'P70206', 'P08121', 'P10107', 'Q3SXB8', 'O35639', 'Q9R1V6', 'Q8CBR6', 'P17553', 'A2ATD1', 'P51670', 'Q9DAN8', 'Q70E20', 'Q640P2', 'P49003', 'P28293', 'Q60716', 'P59384', 'P09056', 'P43488', 'Q9QXT5', 'Q80Z19', 'P50405', 'Q9Z2L7', 'Q8C9W3', 'Q9JKV9', 'Q3U962', 'P57785', 'Q91ZV7', 'P41245', 'Q8BM88', 'O70370', 'P97430', 'P43137', 'Q9D777', 'Q8CD91', 'P97737', 'Q8VCM7', 'D3Z7H8', 'Q8R459', 'Q8BU25', 'P01572', 'Q61245', 'Q3U515', 'Q62005', 'P18340', 'O88632', 'Q61878', 'P07758', 'O35632', 'P27090', 'Q3MI99', 'Q9CQV3', 'Q61092', 'O35598', 'Q499E0', 'O08573', 'Q06186', 'Q9ET39', 'P11088', 'Q80SS5', 'O35674', 'Q8CJ70', 'Q9QYY7', 'P47877', 'Q80T21', 'O35701', 'Q9WUG6', 'Q8CJ69', 'O55123', 'Q6DIB5', 'Q9QY40', 'P33434', 'Q8C4U3', 'P09235', 'Q9JJY9', 'P43432', 'Q9DCQ7', 'P13438', 'P48346', 'P98086', 'Q7TSL0', 'P32766', 'P47993', 'P16294', 'Q62178', 'Q9JL99', 'Q9DAZ2', 'Q80T03', 'P63277', 'P12850', 'P55002', 'Q8BYY9', 'P01582', 'P27005', 'Q66K08', 'P15655', 'Q08731', 'Q04857', 'P47879', 'P19324', 'P34821', 'Q6GQT1', 'P08207', 'A6H584', 'O35464', 'Q8R2Z5', 'F7A4A7', 'P0C7M9', 'Q8VCP9', 'Q07105', 'Q925I7', 'P04401', 'P01573', 'P39039', 'Q9WUU7', 'Q8VHD8', 'O35103', 'Q3UTY6', 'P27467', 'P59511', 'P31955'}


def peptideatlas_fix(html_file_list:list):
    for f in html_file_list:

        if f.split('_')[-1].split('.html')[0] in mouse_uniprotids:
            # print (f)
            html_str = open(f, 'r').read()
            new_html_str = html_str.replace('atlas_build_id=526', 'atlas_build_id=446')
            f_w = open(f,'w')
            f_w.write(new_html_str)
            f_w.close()


if __name__=='__main__':

    html_files = glob('F:/matrisomedb2.0/peptideatlas_test/*.html')

    peptideatlas_fix(html_files)