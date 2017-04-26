def get_fans_list(self, required_page_count=0, time_delay=0.2):
    """
    获取当前用户的粉丝列表
    每个粉丝的信息存储在dict中
    :param required_page_count:0
           time_delay:0.2
    :return: self.fans_list
    """
    fans_url = 'http://weibo.cn/' + str(self.uid) + '/fans'

    # 获取用户粉丝页面
    try:
        first_requests = requests.get(fans_url, headers=headers_for_get, timeout=3)
    except:
        raise Exception, "网络错误，获取粉丝列表失败！"
    first_requests_content = BeautifulSoup(first_requests.content, "lxml")
    if not first_requests_content.find('div', attrs={'class': 'n'}):
        raise Exception, "Cookie失效，获取粉丝列表失败！"

    # 获取第一页粉丝列表
    unit_list = first_requests_content.find_all('table')
    for i in unit_list:
        fans = {}
        try:
            fans['uid'] = i.tr.td.a.attrs['href'].split('u/')[1]
        except:
            continue
        fans['name'] = i.tr.find_all('td')[1].a.get_text()
        # 正则匹配获取粉丝的粉丝数
        pattern = re.compile(r'\d+')
        # 若粉丝是大V，则应匹配第4个标签
        try:
            fans['is_v'] = False
            fans['fans_count'] = int(re.findall(pattern, i.tr.find_all('td')[1].contents[2])[0])
        except:
            fans['fans_count'] = int(re.findall(pattern, i.tr.find_all('td')[1].contents[3])[0])
            fans['is_v'] = True
        self.fans_list.append(fans)

    # 获取粉丝页数
    if first_requests_content.find(attrs={'id': 'pagelist'}):
        page_count = first_requests_content.find(attrs={'id': 'pagelist'}).form.div.contents[-1].strip()
        page_count = page_count.split('/')[1]
        page_count = int(re.findall(pattern, page_count)[0])
        print(page_count)
    else:
        return self.fans_list

    if required_page_count == 0 or required_page_count > page_count:
        min_page_count = page_count
    else:
        min_page_count = required_page_count
    print("将获取", str(min_page_count), "页内容")

    next_url_count = 1
    while next_url_count < min_page_count:
        next_url_count += 1
        next_url = 'http://weibo.cn/' + str(self.uid) + '/fans?page=' + str(next_url_count)
        time.sleep(time_delay)

        # 设置重试次数
        retry_count = 3
        while retry_count != 0:
            retry_count -= 1
            try:
                next_requests = requests.get(next_url, headers=headers_for_get, timeout=3)
                next_requests_content = BeautifulSoup(next_requests.content, "lxml")
                break
            except:
                print("获取" + str(self.uid) + "的粉丝页时失败，正在重试。。。")
            if retry_count == 0:
                raise Exception, "重试次数已完，仍获取" + str(self.uid) + "的粉丝页失败！"

        # 获取当前页的粉丝列表
        unit_list = next_requests_content.find_all('table')
        for i in unit_list:
            fans = {}
            try:
                fans['uid'] = i.tr.td.a.attrs['href'].split('u/')[1]
            except:
                continue
            fans['name'] = i.tr.find_all('td')[1].a.get_text()
            # 正则匹配获取粉丝的粉丝数
            pattern = re.compile(r'\d+')
            try:
                fans['is_v'] = False
                fans['fans_count'] = int(re.findall(pattern, i.tr.find_all('td')[1].contents[2])[0])
            except:
                fans['fans_count'] = int(re.findall(pattern, i.tr.find_all('td')[1].contents[3])[0])
                fans['is_v'] = True
            print(fans['name'])
            print(fans['fans_count'])
            self.fans_list.append(fans)

    return self.fans_list