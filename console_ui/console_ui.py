from time import sleep
from boxpy import boxpy
from getkey import getkey
from collections.abc import Callable
from boxpy.string_width import string_width

def execute(value):
  if isinstance(value, ObserveableValue):
    return execute(value.get_value())
  
  if isinstance(value, ObserveableExpr):
    return execute(value.exec())

  return value

class ObserveableExpr:
  def __init__(self, exec):
    self.exec = exec

class ObserveableValue:
  def __init__(self, default = None, getter = None):
    self.default = default
    self.getter = getter

  def get_value(self):
    return self.getter() if self.getter else self.default

  def exec(self):
    return execute(self)

  # Basic operators
  def __add__(self, other):        return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) + execute(other)))
  def __sub__(self, other):        return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) - execute(other)))
  def __mul__(self, other):        return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) * execute(other)))
  def __div__(self, other):        return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) / execute(other)))
  def __rem__(self, other):        return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) % execute(other)))
  def __truediv__(self, other):    return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) / execute(other)))
  def __floordiv__(self, other):   return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) // execute(other)))
  def __pow__(self, other):        return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) ** execute(other)))
  def __radd__(self, other):       return ObserveableValue(ObserveableExpr(lambda: execute(other) + execute(self.get_value())))
  def __rsub__(self, other):       return ObserveableValue(ObserveableExpr(lambda: execute(other) - execute(self.get_value())))
  def __rmul__(self, other):       return ObserveableValue(ObserveableExpr(lambda: execute(other) * execute(self.get_value())))
  def __rdiv__(self, other):       return ObserveableValue(ObserveableExpr(lambda: execute(other) / execute(self.get_value())))
  def __rrem__(self, other):       return ObserveableValue(ObserveableExpr(lambda: execute(other) % execute(self.get_value())))
  def __rtruediv__(self, other):   return ObserveableValue(ObserveableExpr(lambda: execute(other) / execute(self.get_value())))
  def __rfloordiv__(self, other):  return ObserveableValue(ObserveableExpr(lambda: execute(other) // execute(self.get_value())))
  def __rpow__(self, other):       return ObserveableValue(ObserveableExpr(lambda: execute(other) ** execute(self.get_value())))
  
  # Bitwise operators
  def __lshift__(self, other):  return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) << execute(other)))
  def __rshift__(self, other):  return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) >> execute(other)))
  def __and__(self, other):     return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) & execute(other)))
  def __or__(self, other):      return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) | execute(other)))
  def __xor__(self, other):     return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) ^ execute(other)))
  def __rlshift__(self, other): return ObserveableValue(ObserveableExpr(lambda: execute(other) << execute(self.get_value())))
  def __rrshift__(self, other): return ObserveableValue(ObserveableExpr(lambda: execute(other) >> execute(self.get_value())))
  def __rand__(self, other):    return ObserveableValue(ObserveableExpr(lambda: execute(other) & execute(self.get_value())))
  def __ror__(self, other):     return ObserveableValue(ObserveableExpr(lambda: execute(other) | execute(self.get_value())))
  def __rxor__(self, other):    return ObserveableValue(ObserveableExpr(lambda: execute(other) ^ execute(self.get_value())))
  def __invert__(self, other):  return ObserveableValue(ObserveableExpr(lambda: ~execute(self.get_value())))

  # Comparison
  def __lt__(self, other): return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) < execute(other)))
  def __le__(self, other): return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) <= execute(other)))
  def __gt__(self, other): return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) > execute(other)))
  def __ge__(self, other): return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) >= execute(other)))
  def __eq__(self, other): return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) == execute(other)))
  def __ne__(self, other): return ObserveableValue(ObserveableExpr(lambda: execute(self.get_value()) != execute(other)))

global currently_running_app_do_not_use
currently_running_app_do_not_use = None

def longest_line(lines):
  return max([ string_width(line) for line in lines ])

def combine_strings_horizontal(box1, box2):
  lines1 = box1.split("\n")
  lines2 = box2.split("\n")
  
  box1_width = longest_line(lines1)
  box2_width = longest_line(lines2)
  
  added = []
  
  if len(lines1) == 0:
    return lines2.join("\n")
    
  if len(lines2) == 0: 
    return lines1.join("\n")
  
  for i in range(max(len(lines1), len(lines2))):
    if i >= len(lines1):
      added.append(" " * box1_width + lines2[i].ljust(box2_width))
        
    elif i >= len(lines2):
      added.append(lines1[i].ljust(box1_width) + " " * box2_width)
    
    else:
      added.append(lines1[i].ljust(box1_width) + lines2[i].ljust(box2_width))
          
  return "\n".join(added)

def render_child(child, is_box = False, align_items: str = "column") -> str:
  if type(child) == box or type(child) == text:
    return child.render()
  elif type(child) == tuple or type(child) == list:
    content = ""
    if align_items == "column":
      for i, inner in enumerate(child):
        content += render_child(inner, is_box)
        if i != len(child) - 1:
          content += "\n" if is_box else ""
    elif align_items == "row":
      for inner in child:
        content = combine_strings_horizontal(
          content,
          render_child(inner, is_box)
        )
    return content
  elif type(child) == str:
    return child
  elif type(child) == int:
    return str(child)
  elif isinstance(child, ObserveableValue | ObserveableExpr):
    return str(execute(child))
  elif type(child) == ContextVariable:
    return str(child.get())
  elif type(child) == react:
    return render_child(child.exec(), True)

  raise Exception("Invalid element child", child)

def each(list, callback):
  def inner_loop():
    real_list = list
    if isinstance(list, ContextVariable):
      real_list = list.get()
    
    items = []
    for i, item in enumerate(real_list):
      try:
        items.append(callback(i, item))
      except Exception:
        items.append(callback(item))

    return items
  
  return react(inner_loop)

class react:
  def __init__(self, block):
    self.block = block

  def exec(self):
    return self.block()

def exec_attr(attr):
  if isinstance(attr, react):
    return attr.exec()

  return attr

class text:
  def __init__(self, *content):
    self.content = content

  def render(self):
    return render_child(self.content)

  def __repr__(self) -> str:
    return f"<text>{self.content.__repr__()}</text>"

class box:
  def __init__(self,
               *children,
               width: int | None | react = None,
               height: int | None | react = None,
               margin: int | react = 0,
               padding: int | react = 0,
               border_style: str | react ="single",
               dim_border: bool | react = False,
               text_alignment: str | react ="left",
               float: str | react ="left",
               title_alignment: str | react ="left",
               title: str | react | None =None,
               border_color: str | None | react = None,
               background_color: str | None | react = None,
               align_items: str | react = "column"
    ):
    self.children = children
    self.align_items = align_items
    
    self.width = width
    self.height = height
    self.margin = margin
    self.padding = padding
    self.border_style = border_style
    self.border_color = border_color
    self.dim_border = dim_border
    self.text_alignment = text_alignment
    self.float = float
    self.title_alignment = title_alignment
    self.title = title
    self.background_color = background_color

  def render(self):
    return boxpy(
      render_child(self.children, True, align_items = exec_attr(self.align_items)),
      
      width = exec_attr(self.width),
      height = exec_attr(self.height),
      margin = exec_attr(self.margin),
      padding = exec_attr(self.padding),
      border_style = exec_attr(self.border_style),
      border_color = exec_attr(self.border_color),
      dim_border = exec_attr(self.dim_border),
      text_alignment = exec_attr(self.text_alignment),
      float = exec_attr(self.float),
      title_alignment = exec_attr(self.title_alignment),
      title = exec_attr(self.title),
      background_color = exec_attr(self.background_color),
    )
    
  def __repr__(self) -> str:
    return f"<box>{self.children.__repr__()}</box>"

class ContextVariable(ObserveableValue):
  def __init__(self, initial, app):
    self.__value = initial
    self.__app = app
    super().__init__(getter = lambda: self.__value)

  def set(self, updated):
    if callable(updated):
      self.__value = updated(self.__value)
    else:
      self.__value = updated

    self.__app.render()

  def get(self):
    return self.__value

class EventHandler:
  def __init__(self):
    self.events = {}

  def start_listening(self):
    while True:
      key = getkey()
      self.trigger_event("key", key)

  def on(self, event: str, callback: Callable):
    self.events[event] = self.events.get(event, []) + [ callback ]

  def trigger_event(self, event: str, *args):
    for cb in self.events.get(event, []):
        cb(*args)

def on_key():
  def wrapper(handler):
    if not currently_running_app_do_not_use:
      raise Exception("on_key(...) can only be used inside an application")

    currently_running_app_do_not_use.event_handler.on("key", handler)
    
  return wrapper

class App:
  def __init__(self, handler, state: dict | None = None):
    
    self.event_handler = EventHandler()
    self.handler = handler
    self.state = state
    self.ctx = {}
    
    if state:
      for key, val in state.items():
        self.ctx[key] = ContextVariable(val, self)
    
    global currently_running_app_do_not_use
    currently_running_app_do_not_use = self

    self.vdom = self.handler(self.ctx)
  
  def render(self):
    print("\033[2J\033[H" + render_child(self.vdom, True))

  def start(self):
    self.render()
    self.event_handler.start_listening()

def app(state: dict | None = None):
  def wrapper(main_app):
    app = App(main_app, state)
    app.start()
  
  return wrapper