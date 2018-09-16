# 简易CSV -> XML 转换脚本

## Quick Start

如果没有特殊需要，请直接按照下列步骤操作

1. 将脚本clone到本地

    找一个干净的目录，然后在终端执行`git clone https://github.com/MarkLux/csv2xml4AJ.git`，把脚本clone到本地

2. 准备csv文件

    将需要转换的数据导出为csv文件格式，然后替换修改的字段名（按照自己的定义来修改，最好只使用大小写字母)。举个例子，从神箭手上直接导出的csv数据首行是这样的：

    ```
    爬取时间(__time),爬取链接(__url),房源ID(hid),房源标题(title),国家(country),省份(province),城市(city),纬度（高德地图）(latitude),经度（高德地图）(longitude),房源类型(type),房客数(guests_count),卧室数(bedrooms_count),床位数(beds_count),卫生间数(bathrooms_count),房源介绍(info),床位安排(room_beds),房源照片(photos),参考价格(refer_price),房东来自(host_location),是否是超赞房东(is_superhost),评价数(comment_count),注册时间(register_time),
    ```

    里面包含了很多不必要的中文，尽管在生成时做了中文的过滤，但是最终过滤的效果不够美观，建议还是自己手动按照预想中的定义替换一下，比如改成下面这样:

    ```
    time,url,hid,title,country,province,city,latitude,longitude,type,guestsCount,bedroomsCount,bedsCount,bathroomsCount,info,roomBeds,photos,referPrice,hostLocation,isSuperhost,commentCount,registerTime,
    ```

    最后把这个csv文件放到刚才clone下来的脚本目录下（就是`csv2xml4AJ`这个文件夹）

3. 修改自定义配置

    转换过程中的所有配置项均储存于`settings.py`文件中，各个字段的含义和配置方案参考下面的 **自定义配置说明**, 不过如果你按照第2步给出的例子修改了csv的首行，那么可以略过这一步，直接使用默认的配置;)

4. fire!

    移动到脚本目录下(`cd csv2xml4AJ`)，然后执行下面的命令运行脚本:

    ```
    python transfer.py [csv文件名称]
    ```

    比如你的csv文件名为`airnb_data.csv`，那么就执行:

    ```
    python trasfer.py airnb_data.csv
    ```

5. 获取并格式化结果

    执行脚本后将会实时打印转换进度，执行完毕后结果将保存在同目录下的`result.xml`。但是由于烦人的中文编码问题，这个xml是没有进行格式化的，所以需要自己手动去转换一下。首先找一个编辑器打开这个`result.xml`，然后把里面的内容复制出来，访问[这个转换网站](http://www.bejson.com/otherformat/xml/)，然后把内容粘贴进去，点击格式化，最后再把格式化后的内容复制出来，就是理想中的xml了。

    值得一提的是，如果csv里数据量很大，这个步骤会比较卡顿（网页有可能崩溃），建议先不要使用太多的记录来做尝试，期待后续优化。

## 自定义配置说明

`settings.py`中各个配置变量的说明：

1. `parents`

    用于自定义xml元素层级嵌套关系，目前没用，可忽略

2. `attributes`

    自定义属性标签，字典格式，举例：

    ```
    {
        'hid':'hotel'
    }
    ```

    表示csv文件中的hid字段，是hotel标签的一个属性。因此当读取hid字段时，将不会生成子节点，而是作为一个属性附加到hotel标签上。

3. `spatio_temporal_cols`

    时空属性集合，包含在这个数组里的所有属性都会被单独拿出来放到`SpatioTemporal`标签下，而其他的属性都会被放到`General`标签下。

4. `special_column_types`

    特殊值字段配置。默认情况下csv文件里所有的值都会被当做文本来转换。但如果某些值是json，那么还需要对其解析，转换成对象，然后再转换成嵌套的xml插入父tag。可以在这个dict里配置所有需要特殊处理的字段，例如：

    ```
    {
        'roomBeds': 'json',
        'photos': 'json'
    }
    ```

    表示`roomBeds`和`photos`这两个字段的值是json格式的，需要进一步处理。

    目前特殊处理仅支持json格式，如果需要后续可以进一步拓展。

5. `top_element_tag`

    包裹整个xml文件的最顶级的tag标签名

6. `single_row_tag`

    包裹csv单行文件的tag标签名