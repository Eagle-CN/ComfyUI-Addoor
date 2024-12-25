import ast
import operator as op

class AD_FluxTrainStepMath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Material_Count": ("INT", {"default": 10, "min": 1, "max": 1000000, "step": 1}),
                "Training_Times_Per_Image": ("INT", {"default": 25, "min": 1, "max": 1000000, "step": 1}),
                "Epoch": ("INT", {"default": 4, "min": 1, "max": 1000000, "step": 1}),
                "equation": ("STRING", {"multiline": True, "default": "Material_Count * Training_Times_Per_Image * Epoch"}),
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("Total_Training_Steps", "Steps_Per_Epoch")
    FUNCTION = "calculate"
    CATEGORY = "🌻 Addoor/Utilities"

    def calculate(self, Material_Count, Training_Times_Per_Image, Epoch, equation):
        operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
                     ast.Div: op.floordiv, ast.Pow: op.pow, ast.USub: op.neg}

        def eval_expr(node):
            if isinstance(node, ast.Num):
                return int(node.n)
            elif isinstance(node, ast.BinOp):
                return operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
            elif isinstance(node, ast.UnaryOp):
                return operators[type(node.op)](eval_expr(node.operand))
            elif isinstance(node, ast.Name):
                return {"Material_Count": Material_Count, 
                        "Training_Times_Per_Image": Training_Times_Per_Image, 
                        "Epoch": Epoch}[node.id]
            else:
                raise TypeError(node)

        try:
            total_steps = eval_expr(ast.parse(equation, mode='eval').body)
            steps_per_epoch = total_steps // Epoch
            return (int(total_steps), int(steps_per_epoch))
        except Exception as e:
            print(f"Error in calculation: {e}")
            return (0, 0)

