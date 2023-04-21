from pynomo.nomographer import Nomographer

N_params_1 = {
    'u_min': 45,
    'u_max': 95,
    'function': lambda u: u / 10,
    'title': r'$Age$',
    'tick_levels': 2,
    'tick_text_levels': 1,
}

N_params_2 = {
    'u_min': 1.20,
    'u_max': 2.20,
    'function': lambda u: u,
    'title': r'$Height$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    # 'scale_type': 'linear_smart',
}

N_params_3 = {
    'u_min': 2.8,
    'u_max': 4.4,
    'function': lambda u: u,
    'title': r'$Pi10$',
    'tick_levels': 3,
    'tick_text_levels': 1,
}

block_1_params = {
    'block_type': 'type_2',
    'width': 8.0,
    'height': 8.0,
    'f1_params': N_params_1,
    'f2_params': N_params_2,
    'f3_params': N_params_3,
    'isopleth_values': [[60, 1.84, 'x'], [50, 1.55, 'x'], ['x', 1.95, 3.65]]
}

main_params = {
    'filename':
    'test_nomo.pdf',
    'paper_height':
    10.0,
    'paper_width':
    10.0,
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
