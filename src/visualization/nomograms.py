from pynomo.nomographer import Nomographer

N_params_1 = {
    'u_min': 45,
    'u_max': 95,
    'function': lambda u: 0.004*u,
    'title': r'$Age$',
    'tick_levels': 2,
    'tick_text_levels': 1,
}

N_params_3 = {
    'u_min': 1.20,
    'u_max': 2.20,
    'function': lambda u: 0.15*u,
    'title': r'$Height$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    # 'scale_type': 'linear_smart',
}

N_params_2 = {
    'u_min': 3.1,
    'u_max': 4.1,
    'function': lambda u: (3.0504-0.0262) - u,
    'title': r'$Pi10$',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

block_1_params = {
    'block_type': 'type_1',
    'width': 16.0,
    'height': 8.0,
    'f1_params': N_params_1,
    'f2_params': N_params_2,
    'f3_params': N_params_3,
    'isopleth_values': [[60, 'x', 1.6], [50, 3.55, 'x']]
}

main_params = {
    'filename':
    'test_nomo.pdf',
    'paper_height':
    10.0,
    'paper_width':
    16.0,
    'block_params': [block_1_params],
    'tranformations': [('rotate', 0.01), ('scale paper')],
    'title_str':
    r'$Pi10=c + b1*Age + b2*Height$',
    'extra_texts': [{
        'x': 2.50,
        'y': 9.0,
        'text': 'Female Never Smoker',
        'width': 5,
    }]
}

Nomographer(main_params)
