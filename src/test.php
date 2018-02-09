public function doPost($action, $data)
    {
        $url = $this->host . $action;

        $this->log->info($url);
        $this->log->info($data);

        $ret = Curl::postJSON($url, [], $data);
        $ret = json_decode($ret, true);

        if (empty($ret) || '0' != $ret['code']) {
            if ('2400' == $ret['code']) {
                $this->errorMessage->setCode(ErrorCode::TOKEN_ERROR);
            } else {
                $this->errorMessage->setCode(ErrorCode::EXCEPTION);
                $this->errorMessage->message = $ret['msg'];
            }
            return false;
        }

        return $ret['data'];
    }