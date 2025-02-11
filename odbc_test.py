import pyodbc
import json
import array

con_str ="DRIVER={ODBC Driver 18 for SQL Server};SERVER=10.177.3.78;DATABASE=vectordb;UID=sa;PWD=1_SQLPerf;LongAsMax=yes;Connect Timeout=30;TrustServerCertificate=Yes;LongAsMax=yes;"

cxn = pyodbc.connect(con_str)
cur = cxn.cursor()
cxn.autocommit = True

# Integer
"""
hndl = cur.prepareStatement("declare @v int = ?; SELECT @v as id")
cur.executePreparedStatement(hndl, 1)
cur.executePreparedStatement(hndl, 2)
"""

# Small Vector (string)

hndl = cur.prepareStatement("declare @v vector(1) = ?; SELECT @v as id")
cur.executePreparedStatement(hndl, '[1]')
print(cur.fetchall())
cur.executePreparedStatement(hndl, '[2]')
print(cur.fetchall())


#small vector (json)
"""
hndl = cur.prepareStatement("declare @v vector(1) = ?; SELECT @v as id")
arr1: list[float] = [1.0]
cur.executePreparedStatement(hndl, json.dumps(arr1))
cur.fetchall()
arr2: list[float] = [2.0]
cur.executePreparedStatement(hndl, json.dumps(arr2))
cur.fetchall()
"""

# Execute (Existing Method
"""
qstr = "declare @v vector(1) = ?; SELECT @v as id"
cur.execute(qstr, json.dumps([1.0]))
cur.fetchall()
cur.execute(qstr, json.dumps([2.0]))
cur.fetchall()
"""

vector_query = f"""
                declare @v vector(768) = ?;
                select t.id from vector_search(
                    table = benchmark.vector_768 AS t,
                    column = [vector],
                    similar_to = @v,
                    metric = 'euclidean',
                    top_n = 100
                ) AS s
                order by t.id
            """

vector_str = "[5.9977955e-001,-3.8075708e-002,1.9585741e-001,1.5361838e-001,-3.0363151e-001,-1.5656266e-001,8.5628882e-002,-3.2310346e-001,4.5814607e-001,3.7439802e-001,-7.9910809e-001,-3.8817456e-001,-3.4488007e-001,-5.1276213e-001,-5.5713862e-001,8.1733841e-001,3.6187190e-001,1.2260879e-001,-1.8463045e-001,4.1962963e-001,-1.5076199e-001,4.4040194e-001,6.6226476e-001,2.7633250e-001,-2.2730359e-001,-5.3684306e-001,-6.2783718e-001,5.8355898e-001,1.3336404e-001,2.6816073e-001,1.6654356e-001,1.8393926e-001,-1.1788813e-001,7.4006051e-001,-4.1048962e-001,4.6749231e-001,-1.0577632e-001,3.8179988e-001,3.9497682e-001,7.6636061e-002,7.4511208e-002,2.1377610e-001,3.2279518e-001,3.4711295e-001,1.0487367e-001,-4.5121048e-002,-4.9846119e-001,7.1444109e-002,-2.8534451e-001,5.2747842e-002,-5.7636791e-001,-6.6837937e-001,1.9100878e-001,-5.1111281e-002,-2.6745495e-001,5.3156167e-001,-1.8491144e-001,9.8373878e-001,1.4814475e-001,1.3484030e-002,3.6502352e-001,2.0602469e-001,-6.2730066e-002,3.4110883e-001,3.2216419e-002,1.9145665e-001,1.9704662e-001,4.7838247e-001,-4.4469081e-002,-4.3953348e-002,-1.0124495e-002,1.0318197e+000,1.6857216e-002,5.1048142e-001,-3.1624679e-002,-4.1736302e-001,1.4792714e-001,3.1410402e-001,1.8609481e-001,5.3387359e-002,-8.4357988e-003,-4.7007611e-001,-3.8370860e-001,-2.2109731e-001,-2.6045308e-001,1.6258748e-001,1.6759826e-001,1.1862870e-001,5.9571642e-002,4.4171327e-001,1.7764464e-001,2.2933428e-001,2.9364315e-001,-3.7274447e-001,4.2192522e-001,6.8135577e-001,4.0613838e-002,1.3984668e-001,-7.7681110e-004,-2.7932508e-002,2.4264689e-001,-3.1591243e-001,-3.6703861e-001,6.8895006e-001,3.3070233e-001,-2.6538917e-001,-4.1471191e-002,1.4756104e-001,2.7742907e-001,6.3011956e-001,5.5356425e-001,-3.1703312e-002,4.0938038e-001,7.4308008e-002,1.4264560e-001,-4.6318102e-001,4.9717954e-001,-1.3379550e-001,1.1097339e-001,-8.9173609e-001,3.1040630e-001,-1.4062203e-002,-1.4396366e-001,-2.9340780e-001,5.7858929e-002,3.3102441e-001,7.6907998e-001,-1.0137051e+000,4.3809927e-001,6.7284232e-001,-3.0731526e-001,4.6747380e-001,4.9482310e-001,4.3235826e-001,-1.3134950e-001,4.4986668e-001,3.7593311e-001,7.1316920e-002,9.5404796e-002,-2.8968650e-001,-5.9776228e-002,1.9763045e-001,2.5582319e-001,1.0269628e+000,1.6949998e-001,2.0118529e-001,5.1532570e-002,2.1545807e-001,-1.1531670e-001,3.1187207e-001,2.5224119e-001,-2.5006336e-001,-3.6902225e-001,4.6877959e-001,-6.3426304e-001,3.3982132e-002,-2.5607440e-001,-2.8416577e-001,-1.9679101e-001,3.9122471e-001,8.0807590e-001,2.7020726e-001,-5.1573622e-003,-2.9305041e-001,-5.9449136e-002,2.8194774e-002,4.0674752e-001,5.4605007e-001,3.3612061e-001,1.5536666e-001,-3.0526966e-001,4.2963896e-002,-2.7714127e-001,-1.7953110e-001,-4.2495248e-003,4.9398157e-001,-2.9836226e-001,-5.2178305e-001,5.0255471e-001,4.4807804e-001,3.1841487e-001,4.7542717e-002,-1.7926858e-001,-3.4188426e-001,3.6179882e-001,-8.1805386e-002,4.6926817e-001,-1.1807907e-001,-5.7628286e-001,3.4132987e-001,2.4208808e-001,-1.5096105e-002,1.2200150e+000,-6.9691187e-001,-2.3239252e-001,1.1430018e-001,-1.5628126e-001,1.5654638e-001,-4.9177459e-001,-1.5728390e-001,5.2605045e-001,-4.3521211e-001,-1.4463644e-001,2.6662213e-001,8.3560461e-001,-7.4553794e-001,-9.7848065e-002,6.2875831e-001,-1.0004760e-001,-2.4288870e-001,2.7162436e-001,1.1195856e-001,-2.0287997e-001,7.5073592e-002,-2.5612664e-001,-3.5917190e-001,4.0668604e-001,-7.4388623e-002,4.6924800e-001,-2.3662712e-001,2.1187429e-001,7.0933211e-001,4.8574588e-001,2.8949067e-001,1.1250265e-002,2.6971388e-001,-3.2266974e-001,-7.7331543e-001,1.7966437e-001,2.6881918e-001,4.7858280e-001,3.0053920e-001,-3.2679643e-002,-4.5157415e-001,-2.1067359e-001,1.4211331e-001,-1.9628952e-001,4.6006081e-001,-3.8028546e-002,-2.8824431e-001,5.1126379e-001,6.5087241e-001,5.7835143e-002,3.0018547e-001,4.6559837e-001,-3.2447994e-001,6.5223187e-001,8.2031989e-001,-7.8532100e-002,1.4841558e-001,-1.5741915e-001,7.8207862e-001,-6.5942593e-002,6.5553606e-001,-3.3507377e-001,3.8827053e-001,6.3852024e-001,1.6861190e-001,1.7676486e-001,4.4269156e-002,2.4591400e-001,1.0022594e-001,5.4712653e-001,1.9257501e-001,-1.3076656e-001,-1.6166791e-001,8.4165514e-002,6.1974359e-001,3.5056633e-001,3.2450485e-001,1.4374004e-001,-2.9632139e-001,3.1888939e-002,-1.9975893e-001,-1.1092533e-003,2.3457788e-002,-1.4073889e-001,-1.4822966e-001,-4.3171090e-001,5.3009450e-001,6.0500801e-002,-2.4954507e-001,1.6182812e-002,-2.1229894e-001,-1.5276164e-001,2.2978823e-001,1.3562937e-001,1.0871315e-001,7.3888429e-002,-3.5912716e-001,5.7802141e-001,6.3001597e-001,6.7393541e-001,-6.8759251e-001,6.0650969e-001,6.2095922e-001,-2.1936197e-002,2.0380373e-001,-1.5098572e-002,-2.4615109e-001,-3.1543616e-002,-3.9931974e-001,-2.2979309e-001,6.8612464e-002,-3.0120203e-001,-9.3151465e-002,2.0634980e-001,1.9683771e-001,-1.5940672e-001,-4.9649063e-002,4.3932828e-001,-2.2712477e-001,-2.3230952e-001,6.9776499e-001,5.3889418e-001,6.8848026e-001,2.5468016e-001,-2.5665098e-001,9.7770602e-002,5.3905880e-001,-2.6668018e-001,2.3387514e-001,-4.1181713e-001,2.8988600e-001,6.6160336e-002,-2.1194021e-001,-4.7720708e-003,-8.5909384e-001,8.1064308e-001,9.4853812e-001,-4.3608233e-002,4.8070827e-001,-4.8022890e-001,-1.4925793e-001,5.2658487e-002,3.6054391e-001,-4.0152672e-001,8.9691626e-004,1.8042542e-002,-1.8871192e-002,4.6342701e-001,4.4161987e-001,4.5420733e-001,2.0319493e-001,-2.1260671e-001,1.8793349e-001,-3.9072439e-001,-3.5926172e-001,4.9604017e-002,9.2582874e-002,3.1135929e-001,3.2172683e-001,-4.8577186e-001,-4.6211150e-002,-7.3114090e-002,2.1965986e-001,4.2600554e-001,1.7845275e-001,6.1598897e-001,-2.4323943e-001,-1.0401323e-001,7.0396101e-001,5.7846165e-001,5.5882311e-001,1.4365697e-001,6.1459398e-001,1.2730776e-001,-1.2083922e-001,1.5627162e-001,-1.5011249e-001,-1.2741551e-001,-4.7236401e-001,-1.3706785e-001,7.3853292e-002,-2.4839090e-001,-4.5827231e-001,-3.2419378e-001,1.1564667e-001,2.1701472e-001,-8.5989058e-002,-4.2291638e-002,4.5313793e-001,-1.3236935e-001,-1.6843627e-001,-1.2259813e-001,3.4413564e-001,4.0449131e-001,4.2885059e-001,-4.2357567e-001,-7.1856135e-001,1.1518143e-001,2.3769206e-001,3.9545372e-001,5.3207099e-002,-7.4893549e-002,3.1782802e-002,-4.0741476e-001,6.9979209e-001,7.1356755e-001,-2.5261793e-001,-2.2015426e-002,1.2913640e-001,4.2573687e-001,2.7691096e-001,4.3345466e+000,9.3500197e-002,-7.8272618e-002,-4.5781037e-001,-5.3859270e-001,9.1624290e-002,1.0034734e+000,-3.5869646e-001,3.2366803e-001,-2.5991151e-001,4.1006562e-001,4.3129614e-001,-5.1739317e-001,6.3441420e-001,5.4322028e-001,-4.6237552e-001,7.7336723e-001,-1.8766575e-001,-2.5059670e-001,-2.5389707e-002,-5.3024572e-001,2.6266468e-001,8.7528116e-001,4.9574945e-002,3.7396702e-001,1.2357781e-001,4.8102710e-001,1.2883383e-001,4.2146441e-001,3.2520825e-001,1.1918733e-001,-5.4583233e-002,-4.4132117e-002,-2.0422490e-001,-8.1623541e-003,3.5019197e-002,-7.3933080e-002,-1.7415105e-001,7.9155695e-003,-1.8152320e-001,1.8955809e-001,-8.7871909e-002,-7.7706933e-002,3.7378299e-001,5.1345670e-001,-7.4417394e-001,-3.0798802e-001,3.0373314e-001,-1.1246301e+000,7.7150565e-001,1.0354302e-001,-6.0695823e-002,8.4928058e-002,-4.0778327e-001,-9.4628356e-002,5.8456141e-001,2.5416011e-001,1.2967928e-001,-4.9735144e-001,-6.5802217e-002,-3.7953563e-002,4.2700380e-001,3.8234410e-001,-1.7356332e-001,-5.8333427e-001,2.4491202e-002,4.3801141e-001,6.3955086e-001,1.1056010e-001,-2.9990897e-001,6.8774414e-001,4.1448975e-001,5.5361104e-001,-3.4257045e-001,-2.8479698e-001,4.3611747e-001,-7.9872823e-001,-7.6914176e-002,4.1746473e-001,-1.0169969e-001,-2.7592978e-004,8.9669660e-002,1.2504156e-001,4.3371952e-001,2.1721117e-001,6.3147712e-001,2.8133982e-001,-2.8972754e-001,5.1338702e-001,1.5807804e-001,3.1322928e-003,-2.9875271e-002,1.4090498e-001,-3.5310346e-001,4.0505148e-002,1.6236320e-001,1.1860009e-001,-3.8211114e+000,7.2516423e-001,2.4459885e-001,-3.3890340e-002,1.9967467e-001,-2.3325256e-001,-8.7279521e-002,8.9968777e-001,-3.8342193e-001,4.8438978e-001,5.4870886e-001,-6.6240571e-002,-3.6600193e-001,-1.8909685e-001,-1.1413037e-001,1.5975241e-001,7.6817475e-002,6.9473171e-001,1.7836057e-001,-1.4866522e-001,4.9493963e-001,-2.2207746e-001,-1.2732275e-001,-5.0768304e-001,-5.7749987e-001,6.6197306e-002,-2.0029761e-001,-2.4542058e-001,2.9039866e-001,-2.5708107e-003,-2.1669932e-001,-1.3612406e-001,3.3704585e-001,-4.8890361e-001,1.1326436e-001,3.7209088e-001,2.4462238e-001,-1.9901414e-001,8.3390301e-001,-5.0062526e-002,-3.9620697e-002,3.9153314e-001,5.1662743e-001,8.5824110e-002,8.6676970e-002,3.5648242e-001,-9.8455630e-002,2.5503379e-001,-2.1119413e-001,2.5766315e-002,-3.0697539e-001,4.8689410e-001,1.2583739e-001,3.3152446e-001,3.1176943e-001,-1.4669013e-001,1.4948206e-001,-2.1827947e-001,1.3589771e-001,3.9058048e-002,1.8848188e-001,5.8117665e-002,1.9788884e-001,-3.6638924e-001,-5.8706063e-001,-4.4013560e-001,3.2337558e-001,-2.5538203e-001,3.4173030e-001,-2.9297799e-002,-1.1054790e-001,1.3325898e-001,3.7256229e-001,2.9961476e-001,-2.5441995e-001,5.7080448e-001,-2.6120123e-001,-3.2875293e-001,6.4592212e-001,4.2149283e-002,1.1358386e-001,-3.3828504e-002,-4.2593107e-001,4.1197529e-001,2.0043650e+000,3.5872027e-001,2.0823715e+000,-3.4026769e-001,-2.5774372e-001,3.7622070e-001,-4.3357110e-001,-1.9966391e-001,-1.1348060e-001,2.1131746e-002,-2.4217230e-001,1.4488827e-001,-1.8755688e-001,1.7373005e-002,4.9815878e-001,3.3745784e-001,4.1798168e-001,-6.7663068e-001,-3.9477170e-001,8.3974898e-002,6.2899876e-001,5.7898873e-001,-6.1902204e-003,3.3113769e-001,2.1123095e-001,9.0509646e-002,4.6595812e-001,1.4999820e-001,3.2112021e-003,1.4273624e-001,3.8260996e-001,2.8773639e-001,1.4047785e-001,3.1834376e-001,-1.9845037e-001,-6.1432738e-002,5.8417350e-002,4.4634233e+000,-9.5287554e-002,1.9006418e-001,-4.2237067e-001,2.7845904e-001,8.5154243e-002,4.6227288e-001,-2.8135681e-001,5.9200153e-002,2.6813611e-001,2.5415131e-001,1.1612852e-001,4.0993616e-001,3.4516212e-001,-8.7155141e-002,-2.9796648e-001,2.6170412e-001,3.2653254e-001,2.3601833e-001,7.2843149e-002,-9.7049922e-002,-8.5251257e-002,-8.1190228e-002,-2.2670306e-001,5.7705921e-001,6.0826528e-001,4.1164792e-001,2.6389566e-001,-3.2958347e-002,-5.9371024e-001,-1.9699335e-001,5.1787996e+000,2.8823145e-002,9.9961713e-002,-8.9443326e-002,8.9731671e-002,3.2102457e-001,-9.4717585e-002,-2.8325947e-002,-6.2818307e-001,-1.6880382e-002,-1.3458326e-001,3.1078014e-001,-1.1678414e-001,8.4704831e-002,4.7322534e-002,-4.3453240e-001,-1.9354941e-001,-1.2052882e-001,3.0605292e-001,-7.8872450e-002,8.0746180e-001,-8.3664060e-002,9.1628447e-002,-2.0655921e-001,-5.1012176e-001,1.0450872e-001,-2.1072076e-001,1.2565844e+000,2.8862160e-001,1.1959206e-002,1.6847073e-001,1.7635077e-001,-3.4052070e-002,6.8606472e-001,-2.7735347e-001,-2.7925062e-001,8.9304793e-001,3.2596171e-001,-7.2940491e-002,2.4756281e-001,-7.1020722e-002,5.6525028e-001,-3.1270483e-001,-3.1825626e-001,7.3986775e-003,1.4794032e-001,-2.5254475e-002,3.3783566e-002,-1.0926068e-001,4.3024698e-001,8.5230164e-002,1.6530603e-002,1.0530376e+000,-6.0699925e-002,-7.6596759e-002,3.4200773e-001,7.1919993e-002,-4.3229398e-001,4.8351654e-001,1.9041212e-001,5.3279483e-001,5.0164945e-002,-2.3640630e-001,3.7509203e-001,-9.6249692e-003,2.4990900e-001,9.0530798e-002,-8.7177187e-002,1.2747845e-001,-3.1223014e-001,-2.1230966e-001,-6.1186489e-002,-1.5584634e-001,2.5697672e-001,2.1795192e-001,-2.0213027e-002,9.4056284e-001,2.2877555e-001,3.2708740e-001,-7.0848131e-001,-3.8834634e-001,-6.3948011e-001,-1.4206366e-001,-8.5564733e-002,-4.5649111e-002,4.1884786e-001,-1.9431612e-001,2.7092600e-001,-1.2618807e-001,3.1485632e-001,3.0899879e-001,1.4963606e-001,-2.4107130e-001,4.6819976e-001,-6.5328699e-001,-1.0067512e-001,1.7123019e-002,4.1311368e-001,-2.3812959e-001,1.0457637e-001,2.9315382e-001,3.5532540e-001,3.7650785e-001,-4.2438143e-001,3.4479314e-001,-4.9451238e-001,1.6649939e-001,1.3620184e-001,9.6914954e-002,4.4324702e-001,2.1388429e-001,2.6261023e-001,-4.0379417e-001,-6.5602042e-002,-3.0078310e-001]"

"""
hndl = cur.prepareStatement(vector_query)
cur.executePreparedStatement(hndl, vector_str)
cur.executePreparedStatement(hndl, vector_str)
"""




vector_arr = [5.9977955e-001,-3.8075708e-002,1.9585741e-001,1.5361838e-001,-3.0363151e-001,-1.5656266e-001,8.5628882e-002,-3.2310346e-001,4.5814607e-001,3.7439802e-001,-7.9910809e-001,-3.8817456e-001,-3.4488007e-001,-5.1276213e-001,-5.5713862e-001,8.1733841e-001,3.6187190e-001,1.2260879e-001,-1.8463045e-001,4.1962963e-001,-1.5076199e-001,4.4040194e-001,6.6226476e-001,2.7633250e-001,-2.2730359e-001,-5.3684306e-001,-6.2783718e-001,5.8355898e-001,1.3336404e-001,2.6816073e-001,1.6654356e-001,1.8393926e-001,-1.1788813e-001,7.4006051e-001,-4.1048962e-001,4.6749231e-001,-1.0577632e-001,3.8179988e-001,3.9497682e-001,7.6636061e-002,7.4511208e-002,2.1377610e-001,3.2279518e-001,3.4711295e-001,1.0487367e-001,-4.5121048e-002,-4.9846119e-001,7.1444109e-002,-2.8534451e-001,5.2747842e-002,-5.7636791e-001,-6.6837937e-001,1.9100878e-001,-5.1111281e-002,-2.6745495e-001,5.3156167e-001,-1.8491144e-001,9.8373878e-001,1.4814475e-001,1.3484030e-002,3.6502352e-001,2.0602469e-001,-6.2730066e-002,3.4110883e-001,3.2216419e-002,1.9145665e-001,1.9704662e-001,4.7838247e-001,-4.4469081e-002,-4.3953348e-002,-1.0124495e-002,1.0318197e+000,1.6857216e-002,5.1048142e-001,-3.1624679e-002,-4.1736302e-001,1.4792714e-001,3.1410402e-001,1.8609481e-001,5.3387359e-002,-8.4357988e-003,-4.7007611e-001,-3.8370860e-001,-2.2109731e-001,-2.6045308e-001,1.6258748e-001,1.6759826e-001,1.1862870e-001,5.9571642e-002,4.4171327e-001,1.7764464e-001,2.2933428e-001,2.9364315e-001,-3.7274447e-001,4.2192522e-001,6.8135577e-001,4.0613838e-002,1.3984668e-001,-7.7681110e-004,-2.7932508e-002,2.4264689e-001,-3.1591243e-001,-3.6703861e-001,6.8895006e-001,3.3070233e-001,-2.6538917e-001,-4.1471191e-002,1.4756104e-001,2.7742907e-001,6.3011956e-001,5.5356425e-001,-3.1703312e-002,4.0938038e-001,7.4308008e-002,1.4264560e-001,-4.6318102e-001,4.9717954e-001,-1.3379550e-001,1.1097339e-001,-8.9173609e-001,3.1040630e-001,-1.4062203e-002,-1.4396366e-001,-2.9340780e-001,5.7858929e-002,3.3102441e-001,7.6907998e-001,-1.0137051e+000,4.3809927e-001,6.7284232e-001,-3.0731526e-001,4.6747380e-001,4.9482310e-001,4.3235826e-001,-1.3134950e-001,4.4986668e-001,3.7593311e-001,7.1316920e-002,9.5404796e-002,-2.8968650e-001,-5.9776228e-002,1.9763045e-001,2.5582319e-001,1.0269628e+000,1.6949998e-001,2.0118529e-001,5.1532570e-002,2.1545807e-001,-1.1531670e-001,3.1187207e-001,2.5224119e-001,-2.5006336e-001,-3.6902225e-001,4.6877959e-001,-6.3426304e-001,3.3982132e-002,-2.5607440e-001,-2.8416577e-001,-1.9679101e-001,3.9122471e-001,8.0807590e-001,2.7020726e-001,-5.1573622e-003,-2.9305041e-001,-5.9449136e-002,2.8194774e-002,4.0674752e-001,5.4605007e-001,3.3612061e-001,1.5536666e-001,-3.0526966e-001,4.2963896e-002,-2.7714127e-001,-1.7953110e-001,-4.2495248e-003,4.9398157e-001,-2.9836226e-001,-5.2178305e-001,5.0255471e-001,4.4807804e-001,3.1841487e-001,4.7542717e-002,-1.7926858e-001,-3.4188426e-001,3.6179882e-001,-8.1805386e-002,4.6926817e-001,-1.1807907e-001,-5.7628286e-001,3.4132987e-001,2.4208808e-001,-1.5096105e-002,1.2200150e+000,-6.9691187e-001,-2.3239252e-001,1.1430018e-001,-1.5628126e-001,1.5654638e-001,-4.9177459e-001,-1.5728390e-001,5.2605045e-001,-4.3521211e-001,-1.4463644e-001,2.6662213e-001,8.3560461e-001,-7.4553794e-001,-9.7848065e-002,6.2875831e-001,-1.0004760e-001,-2.4288870e-001,2.7162436e-001,1.1195856e-001,-2.0287997e-001,7.5073592e-002,-2.5612664e-001,-3.5917190e-001,4.0668604e-001,-7.4388623e-002,4.6924800e-001,-2.3662712e-001,2.1187429e-001,7.0933211e-001,4.8574588e-001,2.8949067e-001,1.1250265e-002,2.6971388e-001,-3.2266974e-001,-7.7331543e-001,1.7966437e-001,2.6881918e-001,4.7858280e-001,3.0053920e-001,-3.2679643e-002,-4.5157415e-001,-2.1067359e-001,1.4211331e-001,-1.9628952e-001,4.6006081e-001,-3.8028546e-002,-2.8824431e-001,5.1126379e-001,6.5087241e-001,5.7835143e-002,3.0018547e-001,4.6559837e-001,-3.2447994e-001,6.5223187e-001,8.2031989e-001,-7.8532100e-002,1.4841558e-001,-1.5741915e-001,7.8207862e-001,-6.5942593e-002,6.5553606e-001,-3.3507377e-001,3.8827053e-001,6.3852024e-001,1.6861190e-001,1.7676486e-001,4.4269156e-002,2.4591400e-001,1.0022594e-001,5.4712653e-001,1.9257501e-001,-1.3076656e-001,-1.6166791e-001,8.4165514e-002,6.1974359e-001,3.5056633e-001,3.2450485e-001,1.4374004e-001,-2.9632139e-001,3.1888939e-002,-1.9975893e-001,-1.1092533e-003,2.3457788e-002,-1.4073889e-001,-1.4822966e-001,-4.3171090e-001,5.3009450e-001,6.0500801e-002,-2.4954507e-001,1.6182812e-002,-2.1229894e-001,-1.5276164e-001,2.2978823e-001,1.3562937e-001,1.0871315e-001,7.3888429e-002,-3.5912716e-001,5.7802141e-001,6.3001597e-001,6.7393541e-001,-6.8759251e-001,6.0650969e-001,6.2095922e-001,-2.1936197e-002,2.0380373e-001,-1.5098572e-002,-2.4615109e-001,-3.1543616e-002,-3.9931974e-001,-2.2979309e-001,6.8612464e-002,-3.0120203e-001,-9.3151465e-002,2.0634980e-001,1.9683771e-001,-1.5940672e-001,-4.9649063e-002,4.3932828e-001,-2.2712477e-001,-2.3230952e-001,6.9776499e-001,5.3889418e-001,6.8848026e-001,2.5468016e-001,-2.5665098e-001,9.7770602e-002,5.3905880e-001,-2.6668018e-001,2.3387514e-001,-4.1181713e-001,2.8988600e-001,6.6160336e-002,-2.1194021e-001,-4.7720708e-003,-8.5909384e-001,8.1064308e-001,9.4853812e-001,-4.3608233e-002,4.8070827e-001,-4.8022890e-001,-1.4925793e-001,5.2658487e-002,3.6054391e-001,-4.0152672e-001,8.9691626e-004,1.8042542e-002,-1.8871192e-002,4.6342701e-001,4.4161987e-001,4.5420733e-001,2.0319493e-001,-2.1260671e-001,1.8793349e-001,-3.9072439e-001,-3.5926172e-001,4.9604017e-002,9.2582874e-002,3.1135929e-001,3.2172683e-001,-4.8577186e-001,-4.6211150e-002,-7.3114090e-002,2.1965986e-001,4.2600554e-001,1.7845275e-001,6.1598897e-001,-2.4323943e-001,-1.0401323e-001,7.0396101e-001,5.7846165e-001,5.5882311e-001,1.4365697e-001,6.1459398e-001,1.2730776e-001,-1.2083922e-001,1.5627162e-001,-1.5011249e-001,-1.2741551e-001,-4.7236401e-001,-1.3706785e-001,7.3853292e-002,-2.4839090e-001,-4.5827231e-001,-3.2419378e-001,1.1564667e-001,2.1701472e-001,-8.5989058e-002,-4.2291638e-002,4.5313793e-001,-1.3236935e-001,-1.6843627e-001,-1.2259813e-001,3.4413564e-001,4.0449131e-001,4.2885059e-001,-4.2357567e-001,-7.1856135e-001,1.1518143e-001,2.3769206e-001,3.9545372e-001,5.3207099e-002,-7.4893549e-002,3.1782802e-002,-4.0741476e-001,6.9979209e-001,7.1356755e-001,-2.5261793e-001,-2.2015426e-002,1.2913640e-001,4.2573687e-001,2.7691096e-001,4.3345466e+000,9.3500197e-002,-7.8272618e-002,-4.5781037e-001,-5.3859270e-001,9.1624290e-002,1.0034734e+000,-3.5869646e-001,3.2366803e-001,-2.5991151e-001,4.1006562e-001,4.3129614e-001,-5.1739317e-001,6.3441420e-001,5.4322028e-001,-4.6237552e-001,7.7336723e-001,-1.8766575e-001,-2.5059670e-001,-2.5389707e-002,-5.3024572e-001,2.6266468e-001,8.7528116e-001,4.9574945e-002,3.7396702e-001,1.2357781e-001,4.8102710e-001,1.2883383e-001,4.2146441e-001,3.2520825e-001,1.1918733e-001,-5.4583233e-002,-4.4132117e-002,-2.0422490e-001,-8.1623541e-003,3.5019197e-002,-7.3933080e-002,-1.7415105e-001,7.9155695e-003,-1.8152320e-001,1.8955809e-001,-8.7871909e-002,-7.7706933e-002,3.7378299e-001,5.1345670e-001,-7.4417394e-001,-3.0798802e-001,3.0373314e-001,-1.1246301e+000,7.7150565e-001,1.0354302e-001,-6.0695823e-002,8.4928058e-002,-4.0778327e-001,-9.4628356e-002,5.8456141e-001,2.5416011e-001,1.2967928e-001,-4.9735144e-001,-6.5802217e-002,-3.7953563e-002,4.2700380e-001,3.8234410e-001,-1.7356332e-001,-5.8333427e-001,2.4491202e-002,4.3801141e-001,6.3955086e-001,1.1056010e-001,-2.9990897e-001,6.8774414e-001,4.1448975e-001,5.5361104e-001,-3.4257045e-001,-2.8479698e-001,4.3611747e-001,-7.9872823e-001,-7.6914176e-002,4.1746473e-001,-1.0169969e-001,-2.7592978e-004,8.9669660e-002,1.2504156e-001,4.3371952e-001,2.1721117e-001,6.3147712e-001,2.8133982e-001,-2.8972754e-001,5.1338702e-001,1.5807804e-001,3.1322928e-003,-2.9875271e-002,1.4090498e-001,-3.5310346e-001,4.0505148e-002,1.6236320e-001,1.1860009e-001,-3.8211114e+000,7.2516423e-001,2.4459885e-001,-3.3890340e-002,1.9967467e-001,-2.3325256e-001,-8.7279521e-002,8.9968777e-001,-3.8342193e-001,4.8438978e-001,5.4870886e-001,-6.6240571e-002,-3.6600193e-001,-1.8909685e-001,-1.1413037e-001,1.5975241e-001,7.6817475e-002,6.9473171e-001,1.7836057e-001,-1.4866522e-001,4.9493963e-001,-2.2207746e-001,-1.2732275e-001,-5.0768304e-001,-5.7749987e-001,6.6197306e-002,-2.0029761e-001,-2.4542058e-001,2.9039866e-001,-2.5708107e-003,-2.1669932e-001,-1.3612406e-001,3.3704585e-001,-4.8890361e-001,1.1326436e-001,3.7209088e-001,2.4462238e-001,-1.9901414e-001,8.3390301e-001,-5.0062526e-002,-3.9620697e-002,3.9153314e-001,5.1662743e-001,8.5824110e-002,8.6676970e-002,3.5648242e-001,-9.8455630e-002,2.5503379e-001,-2.1119413e-001,2.5766315e-002,-3.0697539e-001,4.8689410e-001,1.2583739e-001,3.3152446e-001,3.1176943e-001,-1.4669013e-001,1.4948206e-001,-2.1827947e-001,1.3589771e-001,3.9058048e-002,1.8848188e-001,5.8117665e-002,1.9788884e-001,-3.6638924e-001,-5.8706063e-001,-4.4013560e-001,3.2337558e-001,-2.5538203e-001,3.4173030e-001,-2.9297799e-002,-1.1054790e-001,1.3325898e-001,3.7256229e-001,2.9961476e-001,-2.5441995e-001,5.7080448e-001,-2.6120123e-001,-3.2875293e-001,6.4592212e-001,4.2149283e-002,1.1358386e-001,-3.3828504e-002,-4.2593107e-001,4.1197529e-001,2.0043650e+000,3.5872027e-001,2.0823715e+000,-3.4026769e-001,-2.5774372e-001,3.7622070e-001,-4.3357110e-001,-1.9966391e-001,-1.1348060e-001,2.1131746e-002,-2.4217230e-001,1.4488827e-001,-1.8755688e-001,1.7373005e-002,4.9815878e-001,3.3745784e-001,4.1798168e-001,-6.7663068e-001,-3.9477170e-001,8.3974898e-002,6.2899876e-001,5.7898873e-001,-6.1902204e-003,3.3113769e-001,2.1123095e-001,9.0509646e-002,4.6595812e-001,1.4999820e-001,3.2112021e-003,1.4273624e-001,3.8260996e-001,2.8773639e-001,1.4047785e-001,3.1834376e-001,-1.9845037e-001,-6.1432738e-002,5.8417350e-002,4.4634233e+000,-9.5287554e-002,1.9006418e-001,-4.2237067e-001,2.7845904e-001,8.5154243e-002,4.6227288e-001,-2.8135681e-001,5.9200153e-002,2.6813611e-001,2.5415131e-001,1.1612852e-001,4.0993616e-001,3.4516212e-001,-8.7155141e-002,-2.9796648e-001,2.6170412e-001,3.2653254e-001,2.3601833e-001,7.2843149e-002,-9.7049922e-002,-8.5251257e-002,-8.1190228e-002,-2.2670306e-001,5.7705921e-001,6.0826528e-001,4.1164792e-001,2.6389566e-001,-3.2958347e-002,-5.9371024e-001,-1.9699335e-001,5.1787996e+000,2.8823145e-002,9.9961713e-002,-8.9443326e-002,8.9731671e-002,3.2102457e-001,-9.4717585e-002,-2.8325947e-002,-6.2818307e-001,-1.6880382e-002,-1.3458326e-001,3.1078014e-001,-1.1678414e-001,8.4704831e-002,4.7322534e-002,-4.3453240e-001,-1.9354941e-001,-1.2052882e-001,3.0605292e-001,-7.8872450e-002,8.0746180e-001,-8.3664060e-002,9.1628447e-002,-2.0655921e-001,-5.1012176e-001,1.0450872e-001,-2.1072076e-001,1.2565844e+000,2.8862160e-001,1.1959206e-002,1.6847073e-001,1.7635077e-001,-3.4052070e-002,6.8606472e-001,-2.7735347e-001,-2.7925062e-001,8.9304793e-001,3.2596171e-001,-7.2940491e-002,2.4756281e-001,-7.1020722e-002,5.6525028e-001,-3.1270483e-001,-3.1825626e-001,7.3986775e-003,1.4794032e-001,-2.5254475e-002,3.3783566e-002,-1.0926068e-001,4.3024698e-001,8.5230164e-002,1.6530603e-002,1.0530376e+000,-6.0699925e-002,-7.6596759e-002,3.4200773e-001,7.1919993e-002,-4.3229398e-001,4.8351654e-001,1.9041212e-001,5.3279483e-001,5.0164945e-002,-2.3640630e-001,3.7509203e-001,-9.6249692e-003,2.4990900e-001,9.0530798e-002,-8.7177187e-002,1.2747845e-001,-3.1223014e-001,-2.1230966e-001,-6.1186489e-002,-1.5584634e-001,2.5697672e-001,2.1795192e-001,-2.0213027e-002,9.4056284e-001,2.2877555e-001,3.2708740e-001,-7.0848131e-001,-3.8834634e-001,-6.3948011e-001,-1.4206366e-001,-8.5564733e-002,-4.5649111e-002,4.1884786e-001,-1.9431612e-001,2.7092600e-001,-1.2618807e-001,3.1485632e-001,3.0899879e-001,1.4963606e-001,-2.4107130e-001,4.6819976e-001,-6.5328699e-001,-1.0067512e-001,1.7123019e-002,4.1311368e-001,-2.3812959e-001,1.0457637e-001,2.9315382e-001,3.5532540e-001,3.7650785e-001,-4.2438143e-001,3.4479314e-001,-4.9451238e-001,1.6649939e-001,1.3620184e-001,9.6914954e-002,4.4324702e-001,2.1388429e-001,2.6261023e-001,-4.0379417e-001,-6.5602042e-002,-3.0078310e-001]
vector_arr2 = [5.9977955e-001,-3.8075708e-002,1.9585741e-001,1.5361838e-001,-3.0363151e-001,-1.5656266e-001,8.5628882e-002,-3.2310346e-001,4.5814607e-001,3.7439802e-001,-7.9910809e-001,-3.8817456e-001,-3.4488007e-001,-5.1276213e-001,-5.5713862e-001,8.1733841e-001,3.6187190e-001,1.2260879e-001,-1.8463045e-001,4.1962963e-001,-1.5076199e-001,4.4040194e-001,6.6226476e-001,2.7633250e-001,-2.2730359e-001,-5.3684306e-001,-6.2783718e-001,5.8355898e-001,1.3336404e-001,2.6816073e-001,1.6654356e-001,1.8393926e-001,-1.1788813e-001,7.4006051e-001,-4.1048962e-001,4.6749231e-001,-1.0577632e-001,3.8179988e-001,3.9497682e-001,7.6636061e-002,7.4511208e-002,2.1377610e-001,3.2279518e-001,3.4711295e-001,1.0487367e-001,-4.5121048e-002,-4.9846119e-001,7.1444109e-002,-2.8534451e-001,5.2747842e-002,-5.7636791e-001,-6.6837937e-001,1.9100878e-001,-5.1111281e-002,-2.6745495e-001,5.3156167e-001,-1.8491144e-001,9.8373878e-001,1.4814475e-001,1.3484030e-002,3.6502352e-001,2.0602469e-001,-6.2730066e-002,3.4110883e-001,3.2216419e-002,1.9145665e-001,1.9704662e-001,4.7838247e-001,-4.4469081e-002,-4.3953348e-002,-1.0124495e-002,1.0318197e+000,1.6857216e-002,5.1048142e-001,-3.1624679e-002,-4.1736302e-001,1.4792714e-001,3.1410402e-001,1.8609481e-001,5.3387359e-002,-8.4357988e-003,-4.7007611e-001,-3.8370860e-001,-2.2109731e-001,-2.6045308e-001,1.6258748e-001,1.6759826e-001,1.1862870e-001,5.9571642e-002,4.4171327e-001,1.7764464e-001,2.2933428e-001,2.9364315e-001,-3.7274447e-001,4.2192522e-001,6.8135577e-001,4.0613838e-002,1.3984668e-001,-7.7681110e-004,-2.7932508e-002,2.4264689e-001,-3.1591243e-001,-3.6703861e-001,6.8895006e-001,3.3070233e-001,-2.6538917e-001,-4.1471191e-002,1.4756104e-001,2.7742907e-001,6.3011956e-001,5.5356425e-001,-3.1703312e-002,4.0938038e-001,7.4308008e-002,1.4264560e-001,-4.6318102e-001,4.9717954e-001,-1.3379550e-001,1.1097339e-001,-8.9173609e-001,3.1040630e-001,-1.4062203e-002,-1.4396366e-001,-2.9340780e-001,5.7858929e-002,3.3102441e-001,7.6907998e-001,-1.0137051e+000,4.3809927e-001,6.7284232e-001,-3.0731526e-001,4.6747380e-001,4.9482310e-001,4.3235826e-001,-1.3134950e-001,4.4986668e-001,3.7593311e-001,7.1316920e-002,9.5404796e-002,-2.8968650e-001,-5.9776228e-002,1.9763045e-001,2.5582319e-001,1.0269628e+000,1.6949998e-001,2.0118529e-001,5.1532570e-002,2.1545807e-001,-1.1531670e-001,3.1187207e-001,2.5224119e-001,-2.5006336e-001,-3.6902225e-001,4.6877959e-001,-6.3426304e-001,3.3982132e-002,-2.5607440e-001,-2.8416577e-001,-1.9679101e-001,3.9122471e-001,8.0807590e-001,2.7020726e-001,-5.1573622e-003,-2.9305041e-001,-5.9449136e-002,2.8194774e-002,4.0674752e-001,5.4605007e-001,3.3612061e-001,1.5536666e-001,-3.0526966e-001,4.2963896e-002,-2.7714127e-001,-1.7953110e-001,-4.2495248e-003,4.9398157e-001,-2.9836226e-001,-5.2178305e-001,5.0255471e-001,4.4807804e-001,3.1841487e-001,4.7542717e-002,-1.7926858e-001,-3.4188426e-001,3.6179882e-001,-8.1805386e-002,4.6926817e-001,-1.1807907e-001,-5.7628286e-001,3.4132987e-001,2.4208808e-001,-1.5096105e-002,1.2200150e+000,-6.9691187e-001,-2.3239252e-001,1.1430018e-001,-1.5628126e-001,1.5654638e-001,-4.9177459e-001,-1.5728390e-001,5.2605045e-001,-4.3521211e-001,-1.4463644e-001,2.6662213e-001,8.3560461e-001,-7.4553794e-001,-9.7848065e-002,6.2875831e-001,-1.0004760e-001,-2.4288870e-001,2.7162436e-001,1.1195856e-001,-2.0287997e-001,7.5073592e-002,-2.5612664e-001,-3.5917190e-001,4.0668604e-001,-7.4388623e-002,4.6924800e-001,-2.3662712e-001,2.1187429e-001,7.0933211e-001,4.8574588e-001,2.8949067e-001,1.1250265e-002,2.6971388e-001,-3.2266974e-001,-7.7331543e-001,1.7966437e-001,2.6881918e-001,4.7858280e-001,3.0053920e-001,-3.2679643e-002,-4.5157415e-001,-2.1067359e-001,1.4211331e-001,-1.9628952e-001,4.6006081e-001,-3.8028546e-002,-2.8824431e-001,5.1126379e-001,6.5087241e-001,5.7835143e-002,3.0018547e-001,4.6559837e-001,-3.2447994e-001,6.5223187e-001,8.2031989e-001,-7.8532100e-002,1.4841558e-001,-1.5741915e-001,7.8207862e-001,-6.5942593e-002,6.5553606e-001,-3.3507377e-001,3.8827053e-001,6.3852024e-001,1.6861190e-001,1.7676486e-001,4.4269156e-002,2.4591400e-001,1.0022594e-001,5.4712653e-001,1.9257501e-001,-1.3076656e-001,-1.6166791e-001,8.4165514e-002,6.1974359e-001,3.5056633e-001,3.2450485e-001,1.4374004e-001,-2.9632139e-001,3.1888939e-002,-1.9975893e-001,-1.1092533e-003,2.3457788e-002,-1.4073889e-001,-1.4822966e-001,-4.3171090e-001,5.3009450e-001,6.0500801e-002,-2.4954507e-001,1.6182812e-002,-2.1229894e-001,-1.5276164e-001,2.2978823e-001,1.3562937e-001,1.0871315e-001,7.3888429e-002,-3.5912716e-001,5.7802141e-001,6.3001597e-001,6.7393541e-001,-6.8759251e-001,6.0650969e-001,6.2095922e-001,-2.1936197e-002,2.0380373e-001,-1.5098572e-002,-2.4615109e-001,-3.1543616e-002,-3.9931974e-001,-2.2979309e-001,6.8612464e-002,-3.0120203e-001,-9.3151465e-002,2.0634980e-001,1.9683771e-001,-1.5940672e-001,-4.9649063e-002,4.3932828e-001,-2.2712477e-001,-2.3230952e-001,6.9776499e-001,5.3889418e-001,6.8848026e-001,2.5468016e-001,-2.5665098e-001,9.7770602e-002,5.3905880e-001,-2.6668018e-001,2.3387514e-001,-4.1181713e-001,2.8988600e-001,6.6160336e-002,-2.1194021e-001,-4.7720708e-003,-8.5909384e-001,8.1064308e-001,9.4853812e-001,-4.3608233e-002,4.8070827e-001,-4.8022890e-001,-1.4925793e-001,5.2658487e-002,3.6054391e-001,-4.0152672e-001,8.9691626e-004,1.8042542e-002,-1.8871192e-002,4.6342701e-001,4.4161987e-001,4.5420733e-001,2.0319493e-001,-2.1260671e-001,1.8793349e-001,-3.9072439e-001,-3.5926172e-001,4.9604017e-002,9.2582874e-002,3.1135929e-001,3.2172683e-001,-4.8577186e-001,-4.6211150e-002,-7.3114090e-002,2.1965986e-001,4.2600554e-001,1.7845275e-001,6.1598897e-001,-2.4323943e-001,-1.0401323e-001,7.0396101e-001,5.7846165e-001,5.5882311e-001,1.4365697e-001,6.1459398e-001,1.2730776e-001,-1.2083922e-001,1.5627162e-001,-1.5011249e-001,-1.2741551e-001,-4.7236401e-001,-1.3706785e-001,7.3853292e-002,-2.4839090e-001,-4.5827231e-001,-3.2419378e-001,1.1564667e-001,2.1701472e-001,-8.5989058e-002,-4.2291638e-002,4.5313793e-001,-1.3236935e-001,-1.6843627e-001,-1.2259813e-001,3.4413564e-001,4.0449131e-001,4.2885059e-001,-4.2357567e-001,-7.1856135e-001,1.1518143e-001,2.3769206e-001,3.9545372e-001,5.3207099e-002,-7.4893549e-002,3.1782802e-002,-4.0741476e-001,6.9979209e-001,7.1356755e-001,-2.5261793e-001,-2.2015426e-002,1.2913640e-001,4.2573687e-001,2.7691096e-001,4.3345466e+000,9.3500197e-002,-7.8272618e-002,-4.5781037e-001,-5.3859270e-001,9.1624290e-002,1.0034734e+000,-3.5869646e-001,3.2366803e-001,-2.5991151e-001,4.1006562e-001,4.3129614e-001,-5.1739317e-001,6.3441420e-001,5.4322028e-001,-4.6237552e-001,7.7336723e-001,-1.8766575e-001,-2.5059670e-001,-2.5389707e-002,-5.3024572e-001,2.6266468e-001,8.7528116e-001,4.9574945e-002,3.7396702e-001,1.2357781e-001,4.8102710e-001,1.2883383e-001,4.2146441e-001,3.2520825e-001,1.1918733e-001,-5.4583233e-002,-4.4132117e-002,-2.0422490e-001,-8.1623541e-003,3.5019197e-002,-7.3933080e-002,-1.7415105e-001,7.9155695e-003,-1.8152320e-001,1.8955809e-001,-8.7871909e-002,-7.7706933e-002,3.7378299e-001,5.1345670e-001,-7.4417394e-001,-3.0798802e-001,3.0373314e-001,-1.1246301e+000,7.7150565e-001,1.0354302e-001,-6.0695823e-002,8.4928058e-002,-4.0778327e-001,-9.4628356e-002,5.8456141e-001,2.5416011e-001,1.2967928e-001,-4.9735144e-001,-6.5802217e-002,-3.7953563e-002,4.2700380e-001,3.8234410e-001,-1.7356332e-001,-5.8333427e-001,2.4491202e-002,4.3801141e-001,6.3955086e-001,1.1056010e-001,-2.9990897e-001,6.8774414e-001,4.1448975e-001,5.5361104e-001,-3.4257045e-001,-2.8479698e-001,4.3611747e-001,-7.9872823e-001,-7.6914176e-002,4.1746473e-001,-1.0169969e-001,-2.7592978e-004,8.9669660e-002,1.2504156e-001,4.3371952e-001,2.1721117e-001,6.3147712e-001,2.8133982e-001,-2.8972754e-001,5.1338702e-001,1.5807804e-001,3.1322928e-003,-2.9875271e-002,1.4090498e-001,-3.5310346e-001,4.0505148e-002,1.6236320e-001,1.1860009e-001,-3.8211114e+000,7.2516423e-001,2.4459885e-001,-3.3890340e-002,1.9967467e-001,-2.3325256e-001,-8.7279521e-002,8.9968777e-001,-3.8342193e-001,4.8438978e-001,5.4870886e-001,-6.6240571e-002,-3.6600193e-001,-1.8909685e-001,-1.1413037e-001,1.5975241e-001,7.6817475e-002,6.9473171e-001,1.7836057e-001,-1.4866522e-001,4.9493963e-001,-2.2207746e-001,-1.2732275e-001,-5.0768304e-001,-5.7749987e-001,6.6197306e-002,-2.0029761e-001,-2.4542058e-001,2.9039866e-001,-2.5708107e-003,-2.1669932e-001,-1.3612406e-001,3.3704585e-001,-4.8890361e-001,1.1326436e-001,3.7209088e-001,2.4462238e-001,-1.9901414e-001,8.3390301e-001,-5.0062526e-002,-3.9620697e-002,3.9153314e-001,5.1662743e-001,8.5824110e-002,8.6676970e-002,3.5648242e-001,-9.8455630e-002,2.5503379e-001,-2.1119413e-001,2.5766315e-002,-3.0697539e-001,4.8689410e-001,1.2583739e-001,3.3152446e-001,3.1176943e-001,-1.4669013e-001,1.4948206e-001,-2.1827947e-001,1.3589771e-001,3.9058048e-002,1.8848188e-001,5.8117665e-002,1.9788884e-001,-3.6638924e-001,-5.8706063e-001,-4.4013560e-001,3.2337558e-001,-2.5538203e-001,3.4173030e-001,-2.9297799e-002,-1.1054790e-001,1.3325898e-001,3.7256229e-001,2.9961476e-001,-2.5441995e-001,5.7080448e-001,-2.6120123e-001,-3.2875293e-001,6.4592212e-001,4.2149283e-002,1.1358386e-001,-3.3828504e-002,-4.2593107e-001,4.1197529e-001,2.0043650e+000,3.5872027e-001,2.0823715e+000,-3.4026769e-001,-2.5774372e-001,3.7622070e-001,-4.3357110e-001,-1.9966391e-001,-1.1348060e-001,2.1131746e-002,-2.4217230e-001,1.4488827e-001,-1.8755688e-001,1.7373005e-002,4.9815878e-001,3.3745784e-001,4.1798168e-001,-6.7663068e-001,-3.9477170e-001,8.3974898e-002,6.2899876e-001,5.7898873e-001,-6.1902204e-003,3.3113769e-001,2.1123095e-001,9.0509646e-002,4.6595812e-001,1.4999820e-001,3.2112021e-003,1.4273624e-001,3.8260996e-001,2.8773639e-001,1.4047785e-001,3.1834376e-001,-1.9845037e-001,-6.1432738e-002,5.8417350e-002,4.4634233e+000,-9.5287554e-002,1.9006418e-001,-4.2237067e-001,2.7845904e-001,8.5154243e-002,4.6227288e-001,-2.8135681e-001,5.9200153e-002,2.6813611e-001,2.5415131e-001,1.1612852e-001,4.0993616e-001,3.4516212e-001,-8.7155141e-002,-2.9796648e-001,2.6170412e-001,3.2653254e-001,2.3601833e-001,7.2843149e-002,-9.7049922e-002,-8.5251257e-002,-8.1190228e-002,-2.2670306e-001,5.7705921e-001,6.0826528e-001,4.1164792e-001,2.6389566e-001,-3.2958347e-002,-5.9371024e-001,-1.9699335e-001,5.1787996e+000,2.8823145e-002,9.9961713e-002,-8.9443326e-002,8.9731671e-002,3.2102457e-001,-9.4717585e-002,-2.8325947e-002,-6.2818307e-001,-1.6880382e-002,-1.3458326e-001,3.1078014e-001,-1.1678414e-001,8.4704831e-002,4.7322534e-002,-4.3453240e-001,-1.9354941e-001,-1.2052882e-001,3.0605292e-001,-7.8872450e-002,8.0746180e-001,-8.3664060e-002,9.1628447e-002,-2.0655921e-001,-5.1012176e-001,1.0450872e-001,-2.1072076e-001,1.2565844e+000,2.8862160e-001,1.1959206e-002,1.6847073e-001,1.7635077e-001,-3.4052070e-002,6.8606472e-001,-2.7735347e-001,-2.7925062e-001,8.9304793e-001,3.2596171e-001,-7.2940491e-002,2.4756281e-001,-7.1020722e-002,5.6525028e-001,-3.1270483e-001,-3.1825626e-001,7.3986775e-003,1.4794032e-001,-2.5254475e-002,3.3783566e-002,-1.0926068e-001,4.3024698e-001,8.5230164e-002,1.6530603e-002,1.0530376e+000,-6.0699925e-002,-7.6596759e-002,3.4200773e-001,7.1919993e-002,-4.3229398e-001,4.8351654e-001,1.9041212e-001,5.3279483e-001,5.0164945e-002,-2.3640630e-001,3.7509203e-001,-9.6249692e-003,2.4990900e-001,9.0530798e-002,-8.7177187e-002,1.2747845e-001,-3.1223014e-001,-2.1230966e-001,-6.1186489e-002,-1.5584634e-001,2.5697672e-001,2.1795192e-001,-2.0213027e-002,9.4056284e-001,2.2877555e-001,3.2708740e-001,-7.0848131e-001,-3.8834634e-001,-6.3948011e-001,-1.4206366e-001,-8.5564733e-002,-4.5649111e-002,4.1884786e-001,-1.9431612e-001,2.7092600e-001,-1.2618807e-001,3.1485632e-001,3.0899879e-001,1.4963606e-001,-2.4107130e-001,4.6819976e-001,-6.5328699e-001,-1.0067512e-001,1.7123019e-002,4.1311368e-001,-2.3812959e-001,1.0457637e-001,2.9315382e-001,3.5532540e-001,3.7650785e-001,-4.2438143e-001,3.4479314e-001,-4.9451238e-001,1.6649939e-001,1.3620184e-001,9.6914954e-002,4.4324702e-001,2.1388429e-001,2.6261023e-001,-4.0379417e-001,-6.5602042e-002,-3.0078311e-001]
"""
print("vector_arr " + str(id(vector_arr)) +  " vector_arr2 " + str(id(vector_arr2)))
vector_arr = vector_arr2
print("vector_arr " + str(id(vector_arr)) +  " vector_arr2 " + str(id(vector_arr2)))

hndl = cur.prepareStatement(vector_query)
cur.executePreparedStatement(hndl, json.dumps(vector_arr))
#cur.executePreparedStatement(hndl, json.dumps(vector_arr2))  
"""
"""
cur.executePreparedStatement(hndl, json.dumps(vector_arr))
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
cur.executePreparedStatement(hndl, json.dumps(vector_arr))  
"""


