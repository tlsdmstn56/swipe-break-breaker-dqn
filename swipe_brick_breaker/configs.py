from dataclasses import dataclass, asdict
import argparse

@dataclass
class Config:

    window_width: int = 800
    window_height: int = 800
    title: str = "Brick Breaker"
    fps: int = 60
    ball_speed: int = 15
    ball_radius:int = 25

    grid_width:int = 6
    grid_height:int = 9
    
    block_width:int = 100
    block_height:int = 35
    block_border_width:int = 2

    header_height:int = 50
    footer_height:int = 50
    header_footer_line_height:int = 10
    
    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser()

        default_cfg = Config()
        for k, default_val in asdict(default_cfg).items():
            if isinstance(default_val, str):
                help_msg = f"{k} (default: '{default_val}')"
            else:
                help_msg = f'{k} (default: {default_val})'

            parser.add_argument(
                f'--{k}', 
                type=type(default_val), 
                default=default_val, 
                help=help_msg)

        return parser        

    @staticmethod
    def from_args(args: argparse.Namespace):
        kwargs = vars(args)
        return Config(**kwargs)