import textfsmlab
def test_config_int_des():
    '''test config'''
    exprected_r1 = {
        "Gi0/1" : "Connect to PC",
        "Gi0/2" : "Connect to Gi0/1 of R2"
    }
    exprected_r2 = {
        "Gi0/1" : "Connect to Gi0/2 of R1",
        "Gi0/2" : "Connect to Gi0/1 of S1",
        "Gi0/3" : "Connect to WAN"
    }
    exprected_s1 = {
        "Gi0/1" : "Connect to Gi0/2 of R2",
        "Gi1/0" : "Connect to PC"
    }
    assert textfsmlab.config_interface_description_R1() == exprected_r1
    assert textfsmlab.config_interface_description_R2() == exprected_r2
    assert textfsmlab.config_interface_description_S1() == exprected_s1
