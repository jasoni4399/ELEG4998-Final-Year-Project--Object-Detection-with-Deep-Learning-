import torch
import torch.nn as nn
import numpy as np
from collections import Counter
#device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
#print(device)

#    nn.Dropout(0.5)
#    #python
#    #lean_read_config.py
#    test_int=1
#    test_list=[1,2,3]
#    test_dict=dict(key1='value1',key2=0.1)
#
#    #reading
#    from mmengine.config import Config
#
#    cfg=Config.fromfile("lean_read_config.py")
#    print(cfg)
#
#    cfg.test_int
#    cfg["test_int"]
#    #config_sdg.py
#    optimizer=dict(type="SGD",lr=0.1,momentum=0.9,weight_decay=0.0001)
#
#    from mmengine import Config, optim
#    from mmengine.registry import OPTIMIZERS
#
#    import torch.nn as nn
#
#    cfg = Config.fromfile("config_sgd.py")
#
#    model=nn.Conv2d(1,1,1)
#    cfg.optimizer.params=model.parameters()
#    optimizer=OPTIMIZERS.build(cfg.optimizer)
#
#    #config file extend
#    #optimizer_cfg.py
#    optimizer=dict(type="SGD",lr=0.02,momentum=0.9,weight_decay=0.0001)
#    #resnet50.py
#    _base_=['optimizer_cfg.py']
#    model=dict(type="ResNet",depth=50)
#
#    #modify extend
#    _base_ = ['optimizer_cfg.py', 'runtime_cfg.py']
#    model = dict(type='ResNet', depth=50)
#    optimizer = dict(lr=0.01)
#    gpu_ids=[0]
#
#    #delete
#    _base_ = ['optimizer_cfg.py', 'runtime_cfg.py']
#    model = dict(type='ResNet', depth=50)
#    optimizer = dict(_delete_=True,type="SGD",lr=0.01)
#
#    #referencing
#    #refer_base_var.py
#    _base_=['resnet50.py']
#    a={{_base_.model}}
#
#    #modify_base_var.py
#    _base_=['resnet50.py']
#    a=_base_.model
#    a.type='MobileNet'
#
#    cfg=Config.fromfile('modify_base_var.py')
#    print(cfg.a)
#
#    #dump
#    cfg.dump('resnet50_dump.py')
#
#    cfg=Config(dict(a=1,a=2))
#    cfg.dump('dump_dict.py')
#
#    #cld modify config
#    parser.add_argument('--cfg-options',
#                nargs='+',
#                action=DictAction,
#                help='override some settings in the used config, the key-value pair'
#                '...')
#    cfg=Config.fromfile(args.config)
#    if args.cfg_options is not None:
#    cfg.merge_from_dict(args.cfg_options)##
print(Counter([bb for bb in [1,3,4,6]]))