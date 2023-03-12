title: 使用 prettymaps 生成精美地图
slug:  prettymaps-generate-maps
date: 2022-08-14
tags: prettymaps, Python, matplotlib, OpenStreetMap
cover: https://storage.live.com/items/4D18B16B8E0B1EDB!7541?authkey=ALYpzW-ZQ_VBXTU

经过[上次](https://tseing.github.io/sui-sui-nian/2022-08-11-prettymaps-install.html)的屡次踩坑，终于艰难地在 Windows 上安装好了 prettymaps。看着 `pip list` 中的 `prettymaps`，我迫不及待地想试着用 `prettymaps` 生成一些地图，那么就开始吧。

## AttributeError 错误

先运行作者给出的示例代码试验一下：

```py
from prettymaps import *
from matplotlib import pyplot as plt
fig, ax = plt.subplots(figsize = (12, 12), constrained_layout = True)
layers = plot(
    'Praça Ferreira do Amaral, Macau', radius = 1100,
    ax = ax,
    layers = {
            'perimeter': {},
            'streets': {
                'custom_filter': '["highway"~"motorway|trunk|primary|secondary|tertiary|residential|service|unclassified|pedestrian|footway"]',
                'width': {
                    'motorway': 5,
                    'trunk': 5,
                    'primary': 4.5,
                    'secondary': 4,
                    'tertiary': 3.5,
                    'residential': 3,
                    'service': 2,
                    'unclassified': 2,
                    'pedestrian': 2,
                    'footway': 1,
                }
            },
            'building': {'tags': {'building': True, 'landuse': 'construction'}, 'union': False},
            'water': {'tags': {'natural': ['water', 'bay']}},
            'green': {'tags': {'landuse': 'grass', 'natural': ['island', 'wood'], 'leisure': 'park'}},
            'forest': {'tags': {'landuse': 'forest'}},
            'parking': {'tags': {'amenity': 'parking', 'highway': 'pedestrian', 'man_made': 'pier'}}
        },
        drawing_kwargs = {
            'background': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'hatch': 'ooo...', 'zorder': -1},
            'perimeter': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'lw': 0, 'hatch': 'ooo...',  'zorder': 0},
            'green': {'fc': '#D0F1BF', 'ec': '#2F3737', 'lw': 1, 'zorder': 1},
            'forest': {'fc': '#64B96A', 'ec': '#2F3737', 'lw': 1, 'zorder': 1},
            'water': {'fc': '#a1e3ff', 'ec': '#2F3737', 'hatch': 'ooo...', 'hatch_c': '#85c9e6', 'lw': 1, 'zorder': 2},
            'parking': {'fc': '#F2F4CB', 'ec': '#2F3737', 'lw': 1, 'zorder': 3},
            'streets': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 3},
            'building': {'palette': ['#FFC857', '#E9724C', '#C5283D'], 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
        },
        osm_credit = {'color': '#2F3737'}
)
plt.savefig('macao.png')
```

但是拋出了错误，提示 `AttributeError: 'DataFrame' object has no attribute 'crs'`。在 [GitHub](https://github.com/marceloprates/prettymaps/issues/88) 上有人给出了解决方案，原因是 `osmnx` 的版本过低，直接 `pip install osmnx==1.2.1` 就可以解决。

需要注意的是，pip 可能会给出错误信息提示 `osmnx==1.2.1` 与 `prettymaps` 不兼容。但同样给出了已成功安装 `osmnx==1.2.1` 的信息。经过我的尝试，`prettymaps` 是可以正常工作的，所以这条错误信息可能没有什么影响。

## 初窥 prettymaps.plot() 函数

`prettymaps` 是在 `matplotlib` 画布上绘制地图的，所以主要参数与 `matplotlib` 的写法相同，用于调整颜色或文本，不甚重要。而用于生成地图的 `prettymaps.plot()` 函数就比较关键，比较常用参数的就以下几项：

```py
plot(
    # 地图的中心点，可以是地名的字符串，也可以经纬度的元组
    'query',
    # 地图半径，单位为米
    radius = 100,
    # 将 x 轴绑定至画布 x 轴
    ax = ax,
    # OpenStreetMap 地图层信息，若不了解复制示例代码即可
    layers = {'perimeter': {}},
    # 图层样式，如颜色等
    drawing_kwargs = {},
    # 版权信息
    osm_credit = {}
)
```

## 圆形模式

与示例代码相同，只要将 `perimeter` 留空，默认的绘图模式就是圆形模式。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7539?authkey=ALYpzW-ZQ_VBXTU)

<p class='intro'>{location}外滩  The Bund, Shanghai</p>

## 圆角矩形模式

圆角矩形模式下，需要新建一个变量 `dilate` 用于控制圆角半径，并在每一个图层的参数中添加 `'circle': False` 与 `'dilate': dilate` 就能生成圆角矩形地图。

在各个图层中添加键值时要注意括号的嵌套，特别容易出错，可以复制以下代码修改。

```py
dilate = 100
palette=['#F4A460', '#FA8072']
layers = plot(
    (26.08594,119.29199), radius = 400,
    ax = ax,
    layers = {
            'perimeter': {"circle": False, "dilate": dilate},
            'streets': {
                'custom_filter': '["highway"~"motorway|trunk|primary|secondary|tertiary|residential|service|unclassified|pedestrian|footway"]',
                'width': {
                    'motorway': 5,
                    'trunk': 5,
                    'primary': 4.5,
                    'secondary': 4,
                    'tertiary': 3.5,
                    'residential': 3,
                    'service': 3,
                    'unclassified': 3,
                    'pedestrian': 3,
                    'footway': 3,
                },
                'circle': False,
                'dilate': dilate,
            },
            'building': {
                'tags': {
                    'building': True,
                    'landuse': 'construction'
                },
                'union': False,
                'circle': False,
                'dilate': dilate
            },
            'water': {
                'tags': {
                    'natural': ['water', 'bay']
                },
                'circle': False,
                'dilate': dilate
            },
            'green': {
                'tags': {
                    'landuse': 'grass',
                    'natural': ['island', 'wood'],
                    'leisure': 'park'
                },
                'circle': False,
                'dilate': dilate,
            },
            'forest': {
                'tags': {'landuse': 'forest'},
                'circle': False,
                'dilate': dilate,
            },
            'parking': {
                'tags': {
                    'amenity': 'parking',
                    'highway': 'pedestrian',
                    'man_made': 'pier'},
                'circle': False,
                'dilate': dilate
            },
    },
        drawing_kwargs = {
            'background': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'hatch': 'ooo...', 'zorder': -1},
            'perimeter': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'lw': 0, 'hatch': 'ooo...',  'zorder': 0},
            'green': {'fc': '#D0F1BF', 'ec': '#2F3737', 'lw': 1, 'zorder': 1},
            'forest': {'fc': '#64B96A', 'ec': '#2F3737', 'lw': 1, 'zorder': 1},
            'water': {'fc': '#a1e3ff', 'ec': '#2F3737', 'hatch': 'ooo...', 'hatch_c': '#85c9e6', 'lw': 1, 'zorder': 2},
            'parking': {'fc': '#F2F4CB', 'ec': '#2F3737', 'lw': 1, 'zorder': 3},
            'streets': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 3},
            'building': {'palette': palette, 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
        },
        osm_credit = {'color': '#2F3737'}
)
```

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7540?authkey=ALYpzW-ZQ_VBXTU)

<p class='intro'>{location}三坊七巷  Sanfang Qixiang, Fuzhou</p>

## 方形模式

欲使地图布满整个方形画面，需要使用 `matplotlib` 的命令，指定绘制出的 x 与 y 轴范围。只需要在圆角矩形的代码中末插入以下代码：

```py
xmin, ymin, xmax, ymax = layers['perimeter'].bounds
dx, dy = xmax-xmin, ymax-ymin
a = .2
ax.set_xlim(xmin+a*dx, xmax-a*dx)
ax.set_ylim(ymin+a*dy, ymax-a*dy)
```

变量 `a` 表示裁去的四周比例。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7541?authkey=ALYpzW-ZQ_VBXTU)

<p class='intro'>{location}闽江  Min River, Fuzhou</p>

## 进阶操作

但不止如此，我想讨论一些进阶的操作。`layers` 参数指定了绘制的图层，在 `drawing_kwargs` 中可以指定图层的样式，由底至上常见以下几个图层：

- `background` 画布的背景，可以参考圆形模式视图中四个角落的空白；
- `perimeter` 图层的底层，如果没有图层覆盖，就表现为该图层的颜色，可以参考方形模式视图中的浅黄色；
- `green` `forest` `water` 等按字面意思理解即可，若想确定各个图层中 `tags` 所代表的具体事物，见 [OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/Zh-hans:Map_Features)。

`drawing_kwargs` 中的样式参数包括以下几个：

- `fc` 图层的填充颜色；
- `ec` 图层的轮廓颜色；
- `hatch` 图层的填充纹理，具体设置见 [matplolib 文档](https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_style_reference.html)；
- `hatch_c` 图层填充纹理的颜色；
- `alpha` 图层的透明度；
- `lw` 图层轮廓线条的宽度；
- `zorder` 层数，决定了图层之间相互掩盖的关系。

有了以上认识之后，我们就能更加随心所欲地绘制想要的地图了。还有一个额外的小技巧，OpenStreetMap 提供了封闭元素，使用地址描述绘制地点，不设置 `radius` 参数， `prettymaps` 就会自动匹配封闭元素的边界，使用这个方式可以绘制指定场所的示意图、行政区的示意图。

```py
fig, ax = plt.subplots(figsize = (12, 12), constrained_layout = True)

# 画布颜色
fig.patch.set_facecolor('#eee')

# 边界向外扩张
def postprocessing(layers):
    layers['perimeter'] = layers['perimeter'].buffer(10)
    return layers

layers = plot(
    "北京大学, 5号, 颐和园路, 海淀区, 北京市, 100871, 中国",
    ax = ax,
    postprocessing = postprocessing,
    layers = {
            'perimeter': {},
            'streets': {
                'custom_filter': '["highway"~"residential|service|unclassified|pedestrian|footway"]',
                'width': {
                    'residential': 1.5,
                    'service': 1.5,
                    'unclassified': 1,
                    'pedestrian': 1,
                    'footway': 1,
                }
            },
            'building': {
                'tags': {
                    'building': True,
                    'landuse': 'construction'
                },
                'union': False
            },
            'water': {
                'tags': {
                    'natural': ['water']
                }
            },
            'green': {
                'tags': {
                    'landuse': ['grass'],
                    'natural': ['island', 'wood'],
                    'leisure': ['park', 'garden']
                }
            },
            'leisure': {
                'tags': {
                    'leisure': ['pitch', 'playground']
                }
            },
            'parking': {
                'tags': {
                    'amenity': 'parking',
                    'highway': 'pedestrian',
                    'man_made': 'pier'
                }
            },
        },
        drawing_kwargs = {
            'background': {'fc': '#eee', 'lw': 0 , 'zorder': -1},
            'perimeter': {'fc': '#F2F4CB', 'ec': '#2F3737', 'lw': 2, 'linestyle': 'dashed', 'zorder': 0},
            'green': {'fc': '#D0F1BF', 'ec': '#2F3737', 'lw': 0.5, 'zorder': 1},
            'leisure': {'fc': '#aae0cb', 'ec': '#2F3737', 'lw': 0.5, 'zorder': 1},
            'water': {'fc': '#a1e3ff', 'ec': '#2F3737', 'lw': 0.5, 'zorder': 2},
            'parking': {'fc': '#F2F4CB', 'ec': '#2F3737', 'lw': 0.5, 'zorder': 3},
            'streets': {'fc': '#2F3737', 'alpha': 0.7, 'lw': 0, 'zorder': 3},
            'building': {'palette': ['#FFC857', '#E9724C', '#C5283D'], 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
        },
        osm_credit = {'color': '#2F3737'}
)
plt.savefig('pku.png')
```

由于 `prettymaps` 的封闭边界太过于靠近建筑，可以使用 `buffer()` 将边界向外扩张一部分，能获得更好的视觉效果。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7542?authkey=ALYpzW-ZQ_VBXTU)

<p class='intro'>{location}北京大学  Peking University, Beijing</p>

调用相应的图层标签，还可以绘制铁路、地铁线路。以下代码调用了了铁路、地铁、站台并将这些元素各自组合为图层：

```py
'railway': {
    'custom_filter': '["railway"~"rail"]',
    'width': 2,
    'circle': False,
    'dilate': dilate,
},
'subway': {
    'tags': {
        "railway": "subway",
    },
    'circle': False,
    'dilate': dilate,
},
'platform': {
    'tags': {
        'railway': 'platform'
    },
    'circle': False,
    'dilate': dilate,
}
```

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7543?authkey=ALYpzW-ZQ_VBXTU)

<p class='intro'>{location}天津站  Tianjin Railway Station, Tianjin</p>

## 自己的话

不得不说，`prettymaps` 是一款十分优秀的 Python 绘图包，它的操作十分简单，足以让我这样不了解 GIS 的用户迅速入门，绘制出十分惊艳的地图。但在实际使用中，`prettymaps` 还是存在着这样那样的问题，使得它的定位可能只能止步于一个发挥创意的工具，而不能成为一个合适的创作工具。

譬如说，各种各样的用户因为各种各样的需求接触到 `prettymaps`，其中不乏有些用户想为某些场所、学校绘制导览地图，但 `prettymaps` 添加元素的方式不够灵活，这会让这些用户使用起来相当费劲。

`prettymaps` 的数据基于 OpenStreetMap，因为国内这样那样的相关法律法规，注定了 OpenStreetMap 的国内贡献者特别少，这对于开源项目来说几乎是致命的。由于 OpenStreetMap 缺少国内数据，使用 `prettymaps` 绘制国内城市的地图是相当力不从心的。

这方面具体表现为大面积缺失建筑，绘制的地图上十分空旷；缺少海洋、海岸线数据，绘制近海区域时呈现为大片空白等等。

OpenStreetMap 的封闭边界是非常亮眼的功能，在 `prettymaps` 中用字符描述地点就能绘制出行政区、建筑群等等。但从另一个方面考虑，OpenStreetMap 的封闭边界是由用户贡献的，所以在涉边境线、涉敏感地区时务必小心。

总而言之，`prettymaps` 为我们提供了另一个视角，让我们俯瞰日常生活的这座城市，感受建筑布局的美。而 OpenStreetMap 可以说是一个伟大的项目，它借助所有人的力量去描绘我们所生活的这个世界的经纬，这个理念闪耀着国际主义与理想主义的光芒。

{warn begin}悲报：OpenStreetMap 在国内已经被墙，所以 prettymaps 也就完全用不了了 😕
——2023 年 03 月 07 日 志{warn end}